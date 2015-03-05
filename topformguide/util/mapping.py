import json

import conversion
import constants
import rating
import datetime.datetime as datetime
from .. import models as models


def mapPowerRatingFromJson(jsonText):
    """
    Maps JSON data to a PowerRating object.
    :param jsonText: [string] JSON data to populate from
    :return: a fully populated PowerRating object
    """
    data = json.loads(jsonText)
    return mapPowerRating(data)


def mapPowerRating(data, powerRating):
    """
    Maps a dict to a PowerRating object.
    :param data: [dict] data to populate object from
    :return: a fully populated PowerRating object
    """

    powerRating.power = data['power']

    if 'unit' in data:
        powerRating.unit = data['unit']

    if 'rpmLower' in data:
        powerRating.minRpm = data['rpmLower']

    if 'rpmUpper' in data:
        powerRating.minRpm = data['rpmUpper']

    return powerRating


def mapTorque(data):
    return mapPowerRating(data, models.PowerRating())


def mapEngineRating(data):
    return mapPowerRating(data, models.EnginePower())

def mapFuelEconomyFromJson(jsonText):
    data = json.loads(jsonText)
    return mapFuelEconomy(data)

def mapFuelEconomy(data):
    fuelEcon = models.FuelEconomy()
    fuelEcon.amount = data['amount']
    fuelEcon.unit = data['unit']
    fuelEcon.condition = data['condition']
    return fuelEcon


def convertMpgFuelEcon(econRatingInMpg):
    newEconRating = models.FuelEconomy()
    newEconRating.condition = econRatingInMpg.condition
    newEconRating.amount = conversion.mpgToLitresPer100km(econRatingInMpg.amount)
    newEconRating.unit = constants.LITRES_PER_100_KM
    return newEconRating


def mapAndConvertFuelEconomies(econs, variant):
    variant.fuelEconomySet = []
    for e in econs:
        newFuelEcon = mapFuelEconomy(e)
        newFuelEcon.variant = variant
        variant.fuelEconomySet.append(newFuelEcon)
        if newFuelEcon.unit == constants.MILES_PER_GALLON:
            metricised = convertMpgFuelEcon(newFuelEcon)
            variant.fuelEconomySet.append(metricised)
            metricised.variant = variant


def getStdEmission(car):
    if car.fuelType == 'ELECTRIC':
        return 0.0

    bestEmissionData = rating.findMostSuitableRating(car.emissionDataSet)
    if bestEmissionData is None:
        return None
    else:
        return bestEmissionData.amount

def mapVariantFromJson(jsonText):
    """

    :param jsonText:
    :return:
    """
    data = json.loads(jsonText)
    car = models.Variant()
    car.name = data['variants']
    car.seats = data['seats']
    car.doors = data['doors']
    car.body = data['bodyType']
    car.driveType = data['driveType']

    # Engine/power
    car.cylinders = data['engineCylinders']
    car.engineType = data['engineType']
    car.fuelType = data['fuelType']
    car.fuelRange = None
    car.fuelTankCapacity = conversion.convertVolumeToLitres(data['fuelTank'], data['fuelTankUnit'])
    if data['enginePower'] is not None:
        car.enginePower = conversion.convertPowerToKilloWatts(data['enginePower'], data['enginePowerUnit'])
        car.enginePowerRpms = data['enginePowerRpms']
        car.enginePowerRpmsHigh = data['enginePowerRpmsHigh']
    # Torque
    car.torque = data['torque']
    car.torqueRpms = data['torqueRpms']
    car.torqueHigh = data['torqueHighRpms']


    # Transmission
    car.transmission = data['transmission']
    car.speeds = data['transmissionSpeeds']

    # Speed - maximum
    if data['topSpeedUnit'] == constants.MPH:
        car.topSpeed = conversion.milesToKilometres(data['topSpeed'])
    else:
        car.topSpeed = data['topSpeed']

    # Speed - zero to whatever
    if data['secondsToUnit'] == constants.SIXTY_MPH:
        car.zeroTo60mph = data['secondsTo']
    else:
        car.zeroTo100Kph = data['secondsTo']

    # Dimensions - mass
    if data['kerbWeight'] is not None:
        car.kerbWeight = conversion.convertToKilograms(data['kerbWeight'], data['weightUnit'])
    if data['grossWeight'] is not None:
        car.grossWeight = conversion.convertToKilograms(data['grossWeight'], data['weightUnit'])
    if data['tareWeight'] is not None:
        car.tareWeight = conversion.convertToKilograms(data['tareWeight'], data['weightUnit'])
    if data['payload'] is not None:
        car.tareWeight = conversion.convertToKilograms(data['payload'], data['weightUnit'])

    # Dimensions - size/length
    if data['wheelbase'] is not None:
        car.wheelbase = conversion.convertLengthToMillimetres(data['wheelbase'], data['sizeUnit'])
    if data['length'] is not None:
        car.length = conversion.convertLengthToMillimetres(data['length'], data['sizeUnit'])
    if data['width'] is not None:
        car.width = conversion.convertLengthToMillimetres(data['width'], data['sizeUnit'])
    if data['height'] is not None:
        car.width = conversion.convertLengthToMillimetres(data['height'], data['sizeUnit'])

    # Dimensions - volume
    if data['bootVolume'] is not None:
        car.bootVolume = conversion.convertVolumeToLitres(data['bootVolume'], data['volumeUnit'])
    if data['interiorVolume'] is not None:
        car.interiorVolume = conversion.convertVolumeToLitres(data['interiorVolume'], data['volumeUnit'])

    # Fuel econ conversions
    mapAndConvertFuelEconomies(data['fuelConsumption'], car)

    # Emissions and eGo
    car.standardEmissions = getStdEmission(data['emissions'])
    car.eGoRating = rating.calculateEGo(car)

    car.safetyRating = data['safetyRating']
    car.safetyRatingSource = data['safetyRatingSource']
    car.airbags = data['airbags']

    # Add raw data
    dataRaw = models.RawData()
    dataRaw.vairiant = car
    dataRaw.fecthDate = datetime.datetime.parse(data['timestamp'], constants.TIMESTAMP_FORMAT)
    dataRaw.source = data['sourceUrl']
    car.rawDataRecords = []
    car.rawDataRecords.append(dataRaw)

    return (data['make'], data['model'], data['year'], data['country'], car)
