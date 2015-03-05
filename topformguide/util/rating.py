from constants import COMBINED, URBAN, CITY, EXTRA_URBAN, HIGHWAY, MILES_PER_GALLON
import constants
import conversion

RATING_TYPE_ORDER = (COMBINED, URBAN, CITY, EXTRA_URBAN, HIGHWAY)


def checkCarHasEGoPreRequisites(car):
    if car.standardEmissions is None:
        return False
    if car.kerbWeight is None and car.tareWeight is None:
        return False
    if car.torque is None:
        return False
    if car.enginePower is None:
        return False
    if len(car.fuelEcononySet) == 0:
        return False

    return True


def calculateEGo(car):
    if checkCarHasEGoPreRequisites(car) is False:
        return None

    weight = car.kerbWeight
    if car.kerbWeight is None:
        weight = car.tareWeight
    tonnage = weight / 1000.0

    go = (car.enginePower / tonnage) * ((car.torque / 1000) / tonnage)
    kmPerLitre = 100.0 / findMostSuitableRating(car.emissionDataSet, constants.LITRES_PER_100_KM).amount
    ef = tonnage * kmPerLitre
    Efm = ef * (1 - car.standardEmissions / 1000.0)
    return Efm * (1 - go / 50)


def calculateEmissions(car):
    # Find the right fuel econ to base it off
    bestEconData = findMostSuitableRating(car.fuelEcononySet)
    if bestEconData is None:
        return None

    # Convert into L/100km if needed
    if bestEconData.unit is MILES_PER_GALLON:
        bestEconData = conversion.mpgToLitresPer100km(bestEconData)

    # Find km per litre
    kmPerLitre = 100.0 / bestEconData.amount
    return calculateEmissionsForFuel(kmPerLitre, car.fuelType)


def findMostSuitableRating(ratingSet, unit=None):
    for type in RATING_TYPE_ORDER:
        for r in ratingSet:
            if r.type is type:
                if unit is not None and r.unit is unit:
                    return type

    return None


def calculateEmissionsForFuel(kmPerLitre, fuelType):
    if fuelType is constants.ELECTRIC:
        return 0.0
    elif fuelType is constants.DIESEL:
        pass
    elif fuelType is constants.PETROL:
        pass
    elif fuelType is constants.ELECTRIC:
        pass
    else:
        return None