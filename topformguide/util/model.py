"""
A utility module containing functions that help navigate and manipuate
the model objects found in models.py as well as the dicts returned by the
data scrapers.
"""


def findFirstMatching(ratingSet, ratingTypes, unit=None):
    """
    For a given set of ratings and ratings type, find the first match in the set of ratings
    against the earliest rating that matches one of those types in order. E.g. for the rating
    types A, B and C, this function finds the first rating that matches A, and if there is none
    the first rating that matches B (and then C and so on).

    :param ratingSet: [iterable] Either models.FuelEconomny or models.EmissionData to search through
    :param ratingTypes: [iterable] a set of strings defining the ratings types
    :param unit: [string] an additional test, to be a match the ratings unit field must match this unit type.
    Defaults to None
    :return: the matching rating or None if not found.
    """
    for type in ratingTypes:
        rating = findRating(ratingSet, type, unit)
        if rating is not None:
            return rating

    return None


def findRating(ratingSet, ratingType, unit=None):
    """
    Finds the first rating in the rating set with a matching type and unit (if specified)
    :param ratingSet: [iterable] the set of all ratings
    :param ratingType: [string] one of RATING_TYPE_ORDER
    :param unit: type of unit - CO2/km L/100km or MPG. If none then unit match not needed
    :return: a rating with the matching type or unit
    """
    for rating in ratingSet.all():
        if rating.type == ratingType:
            if unit is None or rating.unit == unit:
                return rating
    return None