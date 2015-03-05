from .. import models


class MakeRepository:
    def __init__(self):
        pass

    def findByName(self, name):
        """
        Finds a Make by either a name or a
        :param name:
        :return:
        """
        models.Country.objects.get(pk=name)