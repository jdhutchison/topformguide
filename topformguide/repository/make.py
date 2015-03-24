from .. import models
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class MakeRepository:
    def __init__(self):
        pass

    def findByName(self, name):
        """
        Finds a Make by its name
        :param name:
        :return:
        """
        try:
            return models.Make.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    def findOrCreate(self, makeName):
        """
        Finds an existing Make witha given name, and creates a new Make object in the database
        if none exist.

        :param makeName: the name of the make to find an existing object for or make a new one
        :return: the Make object as saved in the database
        """
        make = self.findByName(makeName)
        if make is not None:
            return make
        else:
            now = datetime.now()
            make = models.Make(name=makeName, created=now, lastUpdated=now)
            make.save()

    def findNamesMakesWithRatedCars(self, bodyType=None):
        """
        Finds the names of all makes that have at leats one variant with an E-Go rating and
        optionally a given body type as well.

        :param bodyType: [string]
        :return: [list[string]] All of the names of the Makes with matching cars
        """
        query = """
                    SELECT DISTINCT m.id as id, m.name as name
                    FROM topformguide_make m
                    INNER JOIN topformguide_carmodel c ON m.id = c.make_id
                    INNER JOIN topformguide_variant v ON c.id = v.model_id
                    WHERE v.eGoRating is not NULL
                """
        if bodyType is not None:
            query = query + " AND v.body = %s"
            makes = models.Make.objects.raw(query.strip() + ';', [bodyType])
        else:
            makes = models.Make.objects.raw(query.strip() + ';')

        return map(lambda m: m.name, makes)