import sys
import traceback
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from topformguide import models
from topformguide.util import mapping
from topformguide.repository import country


class DataLoader:
    def __init__(self, failLog=None):
        self.countryRepository = country.CountryRepository()
        self.logFailures = failLog
        if failLog is True:
            self.failLogFile = open('/files/dev/projects/topformguide/data/reports/failed.json', 'w')
            self.errorFile = open('/files/dev/projects/topformguide/data/reports/failed-errors.log', 'w')

    def __loadRecord(self, json):
        makeName, modelName, year, countryCode, car, rawData = mapping.mapVariantFromJson(json)

        # Load the country
        country = self.countryRepository.findByCode(countryCode)

        # Handle the make and the model
        make, model = self.__findOrCreateMakeAndModel(makeName, modelName, year, country)
        car.model = model

        # Look for existing model and either update OR add data
        existing = self.__findAnyMatchingVariant(car, country)

        if existing is not None:
            dataRecord = car.dataRecords[0]
            dataRecord.variant = existing
            dataRecord.save()
        else:
            now = datetime.now()
            car.created = now
            car.lastUpdated = now
            car.save()
            car.countries.add(country)
            mapping.mapFuelEconomyAndEmissions(car, rawData)
            mapping.mapRawDataRecord(car, rawData, json)
            car.save()
            # print('Added new car\n')

    def __findOrCreateMakeAndModel(self, makeName, modelName, year, country):
        # Find make
        try:
            make = models.Make.objects.get(name=makeName)
        except ObjectDoesNotExist:
            now = datetime.now()
            make = models.Make(name=makeName, created=now, lastUpdated=now)
            make.save()
            print('Made new make for \'%s\'\n' % makeName)

        try:
            model = models.CarModel.objects.get(name=modelName, make=make, year=year)
        except ObjectDoesNotExist:
            now = datetime.now()
            model = models.CarModel(make=make, name=modelName, year=year, created=now, lastUpdated=now)
            model.save()
            model.countries.add(country)
            model.save()
            print('Made new model for %d %s %s\n' % (year, modelName, makeName))

        return make, model

    def __findAnyMatchingVariant(self, variant, country):
        try:
            return models.Variant.objects.get \
                (model=variant.model, name=variant.name, body=variant.body, transmission=variant.transmission,
                 engineType=variant.engineType, cylinders=variant.cylinders, fuelType=variant.fuelType,
                 doors=variant.doors). \
                filter(countries=country)
        except:
            return None

    def __writeFailure(self, json, exc_type, exc_value, exc_traceback):
        if self.logFailures is None or self.logFailures is False:
            return

        self.failLogFile.write('%s\n' % json)

        self.errorFile.write('Record: %s\n' % json)
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=self.errorFile)
        self.errorFile.write('------------------------------------------------------\n')

    def __closeLogs(self):
        if self.logFailures:
            self.failLogFile.close()
            self.errorFile.close()

    def loadCarsFromFile(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()

        self.processCarsAsText(lines)

    def processCarsAsText(self, carData):
        if type(carData).__name__ == 'str':
            carData = carData.split('\n')

        for car in carData:
            try:
                self.__loadRecord(car)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.__writeFailure(car, exc_type, exc_value, exc_traceback)

        self.__closeLogs()
        print('%d cars processed.\n' % len(carData))
