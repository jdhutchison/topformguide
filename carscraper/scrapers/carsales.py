import urllib3
import urlparse
import json
from datetime import datetime
from bs4 import BeautifulSoup
import models
import dictUtils
import sys,traceback
import requests
import time

class CarSalesScraper:
    """A scraper that collects data from redbook.com.au"""

    BASE_URL = 'http://www.carsales.com.au/'
    MAKE_DATA_URI = '/ajax/execute.ashx?SearchUrl=%3fext%3dGroupResult%26N%3d3205%2b3296%26vertical%3dCar%26silo%3dSpec%26base%3d&ajaxMN=AjaxGet&ajaxCN=EndecaSearchProvider,Endeca.Toolkit.Extension&dim=Make&refurl=%3FTabID%253d2807416%2526vertical%253dCar%2526eapi%253d2%2526N%253d3205%252b3296%2526silo%253dSpec%2526Ext%253dGroupResult%2526sort%253ddefault%2526seo%253dtrue%2526seourlbase%253d%252fcars%252fmodels-new%252f'
    MODEL_DATA_URI = '/ajax/execute.ashx?SearchUrl=%3fN%3d[makeid]%2b3205%2b3296%26vertical%3dCar%26silo%3dSpec%26base%3d&ajaxMN=AjaxGet&ajaxCN=EndecaSearchProvider,Endeca.Toolkit.Extension&dim=Model&refurl=%3FTabID%253d2807416%2526vertical%253dcar%2526eapi%253d2%2526N%253d[makeid]%252b3205%252b3296%2526silo%253dspec%2526Ext%253dGroupResult%2526sort%253ddefault%2526seo%253dtrue%2526seourlbase%253d%252fcars%252fmodels-new%252f'
    VARIANT_LIST_URI = '/new-cars/results.aspx?tabid=2207633&Vertical=Car&eapi=2&N=2994+3296+[makeid]+[modelid]&Silo=Spec&Nne=50&tsrc=sr-landing-search&Ns=p_HasPhotos_Int32%7C1%7C%7Cp_IsSpecialOffer_Int32%7C1%7C%7Cp_Year_String%7C1%7C%7Cp_ReleaseMonth_Int32%7C1%7C%7Cp_Make_String%7C0%7C%7Cp_Family_String%7C0#ctl09_p_ctl06_cboModel=[modelid]&ctl09_p_ctl06_cboMake=[makeid]'

    def __init__(self):
        self.cars = []
        self.httpClient = urllib3.PoolManager()
        self.postCarFunction = None
        self.pauseTime = 15
        self.requestSession = requests.Session()
        self.requestSession.mount(CarSalesScraper.BASE_URL, requests.adapters.HTTPAdapter(max_retries=5))

    def getCarData(self):
        response = self.httpClient.request('GET', urlparse.urljoin(self.BASE_URL, self.MAKE_DATA_URI))
        time.sleep(self.pauseTime)
        makes = json.loads(response.data)
        print('%d makes found' % len(makes))
        for make in makes:
            self.findAllModelsForMake(make)

    def findAllModelsForMake(self, make):
        modelsUri = self.MODEL_DATA_URI.replace('[makeid]', make['Value'])
        response = self.httpClient.request('GET', urlparse.urljoin(self.BASE_URL, modelsUri))
        time.sleep(self.pauseTime)
        models = json.loads(response.data)
        print("Found %d model(s) for %s" % (len(models), make['Text']))
        for model in models:
            start = len(self.cars)
            self.findAllVariantsForModel(make['Text'], make['Value'], model)
            count = len(self.cars) - start
            print("%s %s number of variants: %d" % (make['Text'], model['Text'], count))


    def findAllVariantsForModel(self, make, makeId, model):
        variantUri = CarSalesScraper.VARIANT_LIST_URI.replace('[makeid]', makeId).replace('[modelid]', model['Value'])
        url = urlparse.urljoin(self.BASE_URL, variantUri)
        while url is not None:
            response = self.httpClient.request('GET', url)
            dom = BeautifulSoup(response.data)
            time.sleep(self.pauseTime)
            for link in dom.select('div.power'):
                urlFragment = link.get('onclick').split('\'')[1]
                try:
                    self.parseCarData(make, model['Text'], urlFragment)
                except:
                    sys.stderr.write('Error processing variant of %s %s\n' % (make, model['Text']))
                    sys.stderr.write('Processing URL %s\n' % urlFragment)
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_traceback)
                    sys.stderr.write('-------------------------\n', )

            # Handle any pages
            nextLink = dom.select('td.next > a.page')
            if nextLink is not None and len(nextLink) != 0:
                url = urlparse.urljoin(self.BASE_URL, nextLink[0].get('href'))
            else:
                url = None


    def parseCarData(self, make, model, url):
        response = self.requestSession.get(urlparse.urljoin(self.BASE_URL, url), allow_redirects=False)
        time.sleep(self.pauseTime)
        if response.status_code is not 200:
            print('No data for %s %s' % (make, model))
            return

        # If there is no year there is no model data
        dom = BeautifulSoup(response.text)
        header = dom.find('h1')
        if header is None or str(header.string).startswith('Sorry') or \
                str(header.string).startswith('Access'):
            print('No data for %s %s' % (make, model))
            return

        car = models.CarData()
        car.make = make
        car.model = model
        car.country = 'AU'
        car.year = int(header.string[0:4])

        # Find and process each attribute
        dataPoints = self.parseDataPoints(dom.select('section#tab-full-specifications tr'))
        self.processDataPoints(car, dataPoints)

        car.sourceUrl = url
        car.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cars.append(car)
        if self.postCarFunction is not None:
            self.postCarFunction(car)

    def parseDataPoints(self, dataPointsInHtml):
        dataPoints = {}
        for point in dataPointsInHtml:
            for th in point.find_all('th'):
                name = None
                label = th.find('label')
                if label is not None:
                    name = str(label.string)
                else:
                    name = str(th.string)
                value = th.next_sibling.next_sibling.string
                dataPoints[name] = str(value)
        return dataPoints

    def processDataPoints(self, car, points):
        car.variant = self.parseVariantName(points).strip()
        car.bodyType = self.parseBodyType(points['Body Style'])
        car.doors = int(points['Doors'])
        car.seats = int(points['Seat Capacity'])
        car.driveType = self.parseDriveType(points)

        car.transmission = self.parseTransmissionType(points['Generic Gear Type'])
        car.transmissionSpeeds = dictUtils.getTokenFromValueAsInt(points, 'Gears', 0)
        car.engineCylinders = dictUtils.getTokenFromValueAsInt(points, 'Cylinders', 0)
        car.engineType = self.parseEngineType(points)
        car.engineVolume = dictUtils.getTokenFromValueAsInt(points, 'Engine Size (cc)', 0)
        car.engineVolumeUnit = 'cc'
        car.enginePower, car.enginePowerRpm, car.enginePowerRpmHigh = \
            self.parseEnginePower(dictUtils.getValue(points, ['Power', 'Combined Power', 'Alternative Engine Power']))
        car.enginePowerUnit = 'kW'
        car.torque, car.torqueRpm, car.torqueRpmHigh = self.parseEnginePower(dictUtils.getValue(points, ['Torque', 'Alternative Engine Torque']))
        car.fuelTank = dictUtils.getTokenFromValueAsInt(points, 'Fuel Capacity', 0)
        car.fuelTankUnit = 'L'
        if 'Fuel Type' in points:
            car.fuelType = points['Fuel Type'].upper().split()[0]
        car.fuelRange = dictUtils.getTokenFromValueAsInt\
            (points, ['Fuel Average Distance', 'Fuel Minimum Distance', 'Electric Engine Km Range'], 0)
        car.fuelRangeUnit = 'L'

        car.fuelConsumption = self.parseFuelEfficiency(points)
        car.emissions = self.parseEmissions(points)

        car.height = dictUtils.getTokenFromValueAsInt(points, 'Height', 0)
        car.width = dictUtils.getTokenFromValueAsInt(points, 'Width', 0)
        car.length = dictUtils.getTokenFromValueAsInt(points, 'Length', 0)
        car.wheelbase = dictUtils.getTokenFromValueAsInt(points, 'Wheelbase', 0)
        car.lengthUnits = 'mm'
        car.kerbWeight = dictUtils.getTokenFromValueAsInt(points, 'Kerb Weight', 0)
        car.grossWeight = dictUtils.getTokenFromValueAsInt(points, 'Gross Vehicle Mass', 0)
        car.tareWeight = dictUtils.getTokenFromValueAsInt(points, 'Tare Mass', 0)
        car.payload = dictUtils.getTokenFromValueAsInt(points, 'Payload', 0)
        car.weightUnit = 'kg'

        car.bootVolume = dictUtils.getTokenFromValueAsInt(points, 'Boot / Load Space Min (L)', 0)
        car.interiorVolume = dictUtils.getTokenFromValueAsInt(points, 'Boot / Load Space Max (L)', 0)
        car.volumeUnit = 'L'

        if 'Acceleration 0-100km/h' in points:
            car.secondsTo = float(points['Acceleration 0-100km/h'][:-2])
            car.secondsToUnit = '100 kph'
        car.topSpeed = dictUtils.getTokenFromValueAsInt\
            (points, ['Top Speed', 'Electric Engine Top Speed', 'Engine Top Speed'], 0)
        car.topSpeedUnit = 'kph'

        car.airbags = dictUtils.getTokenFromValueAsInt(points, 'Number of Airbags', 0)
        if 'ANCAP Rating' in points and points['ANCAP Rating'] is not None:
            car.safetyRating = int(points['ANCAP Rating'])
            car.safetyRatingSource = 'ANCAP'

    def parseTransmissionType(self, type):
        if type.find('Automatic') >= 0:
            return 'AUTO'
        elif type.find('Sport') >= 0:
            return 'SPORT'
        else:
            return 'MANUAL'

    def parseBodyType(self, bodyType):
        bodyType = bodyType.upper().replace(' ', '_')
        if bodyType.find('HATCH') >= 0:
            return 'HATCHBACK'
        elif bodyType.find('WAGON') >= 0:
            return 'WAGON'
        elif bodyType.find('SUV') >= 0:
            return 'SUV'
        elif bodyType.find('CONVERTIBLE') >= 0:
            return 'CONVERTIBLE'
        elif bodyType.find('COUPE') >= 0:
            return 'COUPE'
        elif bodyType.find('CREWVAN') >= 0:
            return 'VAN'
        elif bodyType.find('SEDAN') >= 0:
            return 'SEDAN'
        elif bodyType.find('CAB_CHASSIS') >= 0:
            return 'CAB_CHASSIS'
        else:
            return bodyType

    def parseEngineType(self, points):
        if 'Generic Engine Type' in points:
           return points['Generic Engine Type'].upper()
        else:
            return points['Engine Type'].upper()

    def parseEnginePower(self, powerData):
        if powerData is None:
            return (None, None, None)

        power = None
        rpmLower = None
        rpmUpper = None

        if powerData.find('@') >= 0:
            parts = powerData.split('@')
            power = float(parts[0].strip()[:-2])
            if parts[1].find('-') == -1:
                rpmLower = int(parts[1][:-3])
                rpmUpper = None
            else:
                rpmData = parts[1][:-3].split('-')
                rpmLower = int(rpmData[0])
                rpmUpper = int(rpmData[1])
        else:
            power = int(powerData[:-3])

        return (power, rpmLower, rpmUpper)

    def parseFuelEfficiency(self, points):
        fuelEconData = []
        for point in points:
            if point.startswith('Fuel Consumption'):
                econ = models.FuelEconomy()
                fuelEconData.append(econ)
                econ.amount = float(points[point].split()[0])
                econ.type = point.replace('Fuel Consumption ', '').upper().replace(' ', '_')
                econ.unit = 'L/100km'

        return fuelEconData

    def parseEmissions(self, points):
        emissionData = []
        for point in points:
            if point.startswith('CO2'):
                ed = models.EmissionLevel()
                emissionData.append(ed)
                ed.amount = float(points[point].split()[0])
                ed.type = point.replace('CO2', '').replace('Emission', '').strip().upper().replace(' ', '_')
                ed.unit = 'g/km'

        return emissionData

    def parseVariantName(self, points):
        if points['Series'].startswith('('):
            return points['Badge']
        elif points['Badge'].startswith('('):
            return points['Series']
        else:
            return '%s %s' % (points['Badge'], points['Series'])

    def parseDriveType(self, points):
        drive = dictUtils.getValueFromAnyKey(points, ['Drive'])
        if drive is None:
            return None
        elif drive.find('4X4') > -1:
            return '4X4'
        elif drive.find('Front') >= 0:
            return 'FRONT'
        elif drive.find('Rear') >= 0:
            return 'REAR'
        elif drive.startswith('All'):
            return 'ALL'
        else:
            return None

