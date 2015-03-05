from .. import models


class CountryRepository:
    def __init__(self):
        pass

    def findByCode(self, code):
        return models.Country.objects.get(pk=code)
