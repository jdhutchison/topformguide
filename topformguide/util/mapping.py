import json
from .. import models as models

def mapPowerRatingFromJson(jsonText):
    """
    Maps JSON data to a PowerRating object.
    :param jsonText: [string] JSON data to populate from
    :return: a fully populated PowerRating object
    """
    data = json.loads(jsonText)
    return mapPowerRating(data)

def mapPowerRating(data):
    """
    Maps a dict to a PowerRating object.
    :param data: [dict] data to populate object from
    :return: a fully populated PowerRating object
    """
    powerRating = models.PowerRating()
    powerRating.power = data['power']
    powerRating.unit = data['unit']

    if 'rpmLower' in data:
        powerRating.minRpm = data['rpmLower']

    if 'rpmUpper' in data:
        powerRating.minRpm = data['rpmUpper']

    return powerRating

def mapFuelEconomyFromJson(jsonText):
    data = json.loads(jsonText)
    return mapFuelEconomy(data)

def mapFuelEconomy(data):
    fuelEcon = models.FuelEconomy()
    fuelEcon.amount = data['amount']
    fuelEcon.unit = data['unit']
    fuelEcon.condition = data['condition']
    return fuelEcon

def mapVariantFromJson(jsonText):
    """

    :param jsonText:
    :return:
    """
    data = json.loads(jsonText)
    car = models.Variant()
    car.name = data['variants']
    car.seats = data['seats']

    # Fuel econ conversions
    for econ in data['fuelConsumption']:
        fuelEcon = mapFuelEconomy(econ)
        fuelEcon.vairant = car


    car.created = data['timestamp']

    return (data['make'], data['model'], data['year'], car)