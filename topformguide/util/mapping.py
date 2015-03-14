import json
from datetime import datetime

from topformguide.util import conversion
from topformguide.util import constants
from topformguide.util import calculations
from topformguide import models


def mapFuelEconomyFromJson(jsonText):
    data = json.loads(jsonText)
    return mapFuelEconomy(data)

def mapFuelEconomy(data):
    fuelEcon = models.FuelEconomy()
    fuelEcon.amount = data['amount']
    fuelEcon.unit = data['unit']
    fuelEcon.type = data['type']
    return fuelEcon


def convertMpgFuelEcon(econRatingInMpg):
    newEconRating = models.FuelEconomy()
    newEconRating.type = econRatingInMpg['type']
    newEconRating.amount = conversion.mpgToLitresPer100km(econRatingInMpg['amount'])
    newEconRating.unit = constants.LITRES_PER_100_KM
    newEconRating.calculated = True
    return newEconRating

def convertEmissionData(data):
    emssionRating = models.EmissionData()
    emssionRating.type = data['type']
    emssionRating.amount = data['amount']
    emssionRating.calculated = False
    emssionRating.unit = data['unit']
    return emssionRating

def mapAndConvertFuelEconomies(econs, variant):
    for e in econs:
        newFuelEcon = mapFuelEconomy(e)
        newFuelEcon.variant = variant
        variant.fuelEconomySet.add(newFuelEcon)
        if newFuelEcon.unit == constants.MILES_PER_GALLON:
            metricised = convertMpgFuelEcon(newFuelEcon)
            variant.fuelEconomySet.add(metricised)
            metricised.variant = variant


    # If there is no combined rating then create one if possible
    if calculations.findRating(variant.fuelEconomySet, constants.COMBINED, constants.LITRES_PER_100_KM) is None:
        averaged = models.FuelEconomy()
        averaged.amount = calculations.calculateCombinedFuelRating(variant)
        averaged.type = constants.COMBINED
        averaged.unit = constants.LITRES_PER_100_KM
        averaged.vairant = variant
        averaged.calculated = True
        if averaged.amount is not None:
            variant.fuelEconomySet.add(averaged)




def mapEmissions(emissions, variant):
    emissionDataSet = []
    for e in emissions:
        newEmissionData = convertEmissionData(e)
        variant.emissionDataSet.add(newEmissionData)
        newEmissionData.variant = variant

    # For each fuel econ type
    for econ in variant.fuelEconomySet.all():
        # If it is l/100kn
        if econ.unit == constants.LITRES_PER_100_KM:
            # find matching emission
            matchingEmission = calculations.findRating \
                (variant.fuelEconomySet, constants.COMBINED, constants.LITRES_PER_100_KM)
            if matchingEmission is None:
                newEmissionData = convertFuelEconomyToEmissions(econ, variant.fuelType)
                variant.emissionDataSet.add(newEmissionData)
                newEmissionData.variant = variant

def convertFuelEconomyToEmissions(fuelEconomy, fuelType):
    emissions = models.EmissionData()
    emissions.type = fuelEconomy.type
    emissions.unit = constants.CO2_PER_KILOMETRE
    emissions.calculated = True
    emissions.amount = calculations.calculateEmissionForFuelEconomy(fuelEconomy, fuelType)
    return emissions

def getStdEmission(car):
    if car.fuelType == 'ELECTRIC':
        return 0.0

    bestEmissionData = calculations.findRating(car.emissionDataSet, constants.COMBINED)
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
    car.name = data['variant']
    car.seats = data['seats']
    car.doors = data['doors']
    car.body = data['bodyType']
    car.driveType = data['driveType']

    # Engine/power
    car.cylinders = data['engineCylinders']
    car.engineType = data['engineType']
    car.fuelType = data['fuelType']
    car.fuelRange = conversion.convertDistanceToKilometres(data['fuelRange'], data['fuelRangeUnit'])
    car.fuelTankCapacity = conversion.convertVolumeToLitres(data['fuelTank'], data['fuelTankUnit'])
    if data['enginePower'] is not None:
        car.enginePower = conversion.convertPowerToKilloWatts(data['enginePower'], data['enginePowerUnit'])
        car.enginePowerRpms = data['enginePowerRpm']
        car.enginePowerRpmsHigh = data['enginePowerRpmHigh']
    # Torque
    car.torque = data['torque']
    car.torqueRpms = data['torqueRpm']
    car.torqueRpmsHigh = data['torqueRpmHigh']


    # Transmission
    car.transmission = data['transmission']
    car.speeds = data['transmissionSpeeds']

    # Speed - maximum
    if data['topSpeedUnit'] == constants.MILES_PER_HOUR:
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
        car.kerbWeight = conversion.convertMassToKilograms(data['kerbWeight'], data['weightUnit'])
    if data['grossWeight'] is not None:
        car.grossWeight = conversion.convertMassToKilograms(data['grossWeight'], data['weightUnit'])
    if data['tareWeight'] is not None:
        car.tareWeight = conversion.convertMassToKilograms(data['tareWeight'], data['weightUnit'])
    if data['payload'] is not None:
        car.tareWeight = conversion.convertMassToKilograms(data['payload'], data['weightUnit'])

    if car.kerbWeight is None:
        car.kerbWeight = calculations.calculateKerbWeight(car)
        car.kerbWeigthCalculated = True
    else:
        car.kerbWeigthCalculated = False

    # Dimensions - size/length
    if data['wheelbase'] is not None:
        car.wheelbase = conversion.convertLengthToMillimetres(data['wheelbase'], data['lengthUnits'])
    if data['length'] is not None:
        car.length = conversion.convertLengthToMillimetres(data['length'], data['lengthUnits'])
    if data['width'] is not None:
        car.width = conversion.convertLengthToMillimetres(data['width'], data['lengthUnits'])
    if data['height'] is not None:
        car.width = conversion.convertLengthToMillimetres(data['height'], data['lengthUnits'])

    # Dimensions - volume
    if data['bootVolume'] is not None:
        car.bootVolume = conversion.convertVolumeToLitres(data['bootVolume'], data['volumeUnit'])
    if data['interiorVolume'] is not None:
        car.interiorVolume = conversion.convertVolumeToLitres(data['interiorVolume'], data['volumeUnit'])

    car.safetyRating = data['safetyRating']
    car.safetyRatingSource = data['safetyRatingSource']
    car.airbags = data['airbags']

    return (data['make'], data['model'], data['year'], data['country'], car, data)


def mapFuelEconomyAndEmissions(variant, data):
    # Fuel econ conversions
    mapAndConvertFuelEconomies(data['fuelConsumption'], variant)

    # Emissions and eGo
    mapEmissions(data['emissions'], variant)
    variant.standardEmissions = getStdEmission(variant)
    variant.eGoRating = calculations.calculateEGo(variant)


def mapRawDataRecord(car, data, text):
    dataRaw = models.RawData()
    dataRaw.variant = car
    dataRaw.fetchDate = datetime.strptime(data['timestamp'], constants.TIMESTAMP_FORMAT)
    dataRaw.source = data['sourceUrl']
    dataRaw.data = text
    car.rawDataRecords.add(dataRaw)
