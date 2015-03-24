from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from topformguide.models import CarModel


class ModelRepository:
    MODELS_WITH_RATED_CARS_SQL = """
        FROM topformguide_make m
        INNER JOIN topformguide_carmodel c ON m.id = c.make_id
        INNER JOIN topformguide_variant v ON c.id = v.model_id
        WHERE v.eGoRating is not NULL
        AND m.name = %s
        ORDER BY c.name, c.year;
    """

    """
    Contains functions to work with and easily query models in DB without need
    to use Django or SQL alchemy API.
    """

    def findByMakeNameYearAndCountry(self, make, modelSlug, year, country):
        """

        :param modelSlug: the slug version of the name of the model
        :return: The matchig model
        """
        try:
            return CarModel.objects.find(name=modelSlug, make=make, year=year, countries__code=country)
        except ObjectDoesNotExist:
            return None

    def findOrCreate(self, make, modelName, year, country):
        """
        Finds a model matching the unique combination of make, model name, year and country and
        if one does not exist then it is created.
        :param make:
        :param modelName:
        :param year:
        :param country
        :return: [models.CarModel] an existing CarModel or a brand new one.
        """
        model = self.findByMakeNameYearAndCountry(make, modelName, year, country)
        if model is None:
            now = datetime.now()
            model = CarModel(make=make, name=modelName, year=year, created=now, lastUpdated=now)
            model.save()
            model.countries.add(country)
            model.save()

        return model

    def findModelNamesWithCarsWithRatingsByMake(self, makeName):
        """

        :param makeName:
        :param modelName:
        :return:
        """
        query = "SELECT DISTINCT c.id as id, c.name as name " + ModelRepository.MODELS_WITH_RATED_CARS_SQL
        models = CarModel.objects.raw(query, [makeName])
        return map(lambda m: m.name, models)

    def getModelsByMake(make):
        """

        :param make:
        :return:
        """
        return CarModel.objects.filter(make__name__iexact=make) \
            .filter(variants__eGoRating__isNull=False).order_by('name', 'year').all()