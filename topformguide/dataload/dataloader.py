import sys
import traceback

from .. import models
from util import mapping
from repository import country
import datetime.datetime


class DataLoader:
    def __init__(self):
        self.countryRepository = country.CountryRepository()

    def __loadRecord(self, json):
        makeName, modelName, year, countryCode, car = mapping.mapVariantFromJson(json)

        # Load the country
        country = self.countryRepository.findByCode(countryCode)

        # Handle the make and the model
        make, model = self.__findOrCreateMakeAndModel(makeName, modelName, year, country)
        car.model = model
        car.countries.add(country)

        # Look for existing model and either update OR add data
        existing = self.__findAnyMatchingVariant(car, country)

        if existing is not None:
            dataRecord = car.dataRecords[0]
            dataRecord.variant = existing
            dataRecord.save()
        else:
            now = datetime.datetime.now()
            car.created = now
            car.lastUpdated = now
            car.save()
            # print('Added new car\n')

    def __findOrCreateMakeAndModel(self, makeName, modelName, year, country):
        # Find make
        make = models.Make.objects.get(name=makeName)
        if make is None:
            now = datetime.datetime.now()
            make = models.Make(name=makeName, create=now, lastUpdated=now)
            make.save()
            print('Made new make for \'%s\'\n' % makeName)

        model = models.CarModel.objects.get(name=modelName, make=make, year=year).filter(countries=country)
        if model is None:
            now = datetime.datetime.now()
            model = models.CarModel(make=make, name=modelName, year=year, created=now, lastUpated=now)
            model.countries.add(country)
            model.save()
            print('Made new model for %d %s %s\n' % year, modelName, makeName)

        return make, model

    def __findAnyMatchingVariant(self, variant, country):
        return models.Variant.objects.get \
            (model=variant.model, name=variant.name, body=variant.body, transmission=variant.transmission,
             engineType=variant.engineType, cylinders=variant.cylinders, fuelType=variant.fuelType,
             doors=variant.doors). \
            filter(countries=country)

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
                sys.stderr.write('Error for record %s:\n', car)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

        print(len(carData) + ' cars processed.\n')
