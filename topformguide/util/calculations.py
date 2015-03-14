from topformguide.util.constants import COMBINED, URBAN, CITY, EXTRA_URBAN, HIGHWAY, MILES_PER_GALLON
from topformguide.util import conversion
from topformguide.util import constants

RATING_TYPE_ORDER = (COMBINED, URBAN, CITY, EXTRA_URBAN, HIGHWAY)

# Fuel volume to mass constants
PETROL_MASS_1L = 0.73722
DIESEL_MASS_1L = 0.8508
LPG_MASS_1L = 0.493
DRIVER_MASS = 75 # mass of a driver in kg

# Fuel type to carbon dioxide per litre, in grams
PETROL_CO2_PER_LITRE = 2392
LPG_CO2_PER_LITRE = 1665
DIESEL_CO2_PER_LITRE = 2640

def checkCarHasEGoPreRequisites(car):
    if car.standardEmissions is None:
        return False
    if car.kerbWeight is None:
        return False
    if car.torque is None:
        return False
    if car.enginePower is None:
        return False
    if findRating(car.fuelEconomySet, constants.COMBINED, constants.LITRES_PER_100_KM) is None:
        return False

    return True


def calculateEGo(car):
    if checkCarHasEGoPreRequisites(car) is False:
        return None

    tonnage = car.kerbWeight / 1000.0
    combinedL100km = findRating(car.fuelEconomySet, constants.COMBINED, constants.LITRES_PER_100_KM).amount
    kmPerLitre = 100.0 / combinedL100km

    go = car.enginePower / tonnage * (car.torque / 1000) / tonnage
    ef = tonnage * kmPerLitre
    Efm = ef * (1 - car.standardEmissions / 1000.0)
    return Efm * (1 + go / 50)


def calculateEmissions(car):
    # Find the right fuel econ to base it off
    bestEconData = findMostSuitableRating(car.fuelEcononySet)
    if bestEconData is None:
        return None

    return calculateEmissionForFuelEconomy(bestEconData, car.fuelType)

def calculateEmissionForFuelEconomy(fuelEcon, fuelType):
    """
    For a given fuel economy (either L/100km or MPG) calculate how much carbon dioxide is
    created for each kilometre of travel at that level of fuel consumption

    :param fuelEcon: [FuelEconomy]
    :param fuelType [string] the type of fuel: must be one of ELECTRIC, LPG, PETROL or DIESEL
    :return: CO2 per kilometre for that fuel economy data, or None if either param is None
    """
    if fuelEcon is None or fuelType is None:
        return None

    # Convert into L/100km if needed
    if fuelEcon.unit is MILES_PER_GALLON:
        fuelEcon = conversion.mpgToLitresPer100km(fuelEcon)

    # Find km per litre
    kmPerLitre = 100.0 / fuelEcon.amount
    return calculateEmissionsForFuel(kmPerLitre, fuelType)

def findMostSuitableRating(ratingSet, unit=None):
    return findFirstMatching(ratingSet, RATING_TYPE_ORDER, unit)

def findFirstMatching(ratingSet, ratingTypes, unit=None):
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

def calculateEmissionsForFuel(kmPerLitre, fuelType):
    """
    Determines how many grams of carbon dioxide is produced per kilometre.

    :param kmPerLitre: [float] how many km per litre a vehicle goes
    :param fuelType: [string] what type of fuel - ELECTRIC, LPG, PETROL or DIESEL. Anything else returns None
    :return: The Co2 produced per kilometre, based on fuel type
    """
    if fuelType is constants.ELECTRIC:
        return 0.0
    elif fuelType is constants.DIESEL:
        return round(DIESEL_CO2_PER_LITRE / kmPerLitre, 0)
    elif fuelType is constants.PETROL:
        return round(PETROL_CO2_PER_LITRE / kmPerLitre, 0)
    elif fuelType is constants.LPG:
        return round(LPG_CO2_PER_LITRE / kmPerLitre, 0)
    else:
        return None


def calculateKerbWeight(car):
    """
    Calculates the Kerb Weight fro the Tare Weight for a car, by calculating the
    mass of half a tank of fuel, pus a 75kg driver.

    :param car: [models.Variant] which vehicle to calculate for
    :return: [float] Kerb Weight mass in kilograms, or None if not enough data available to
    calculate correctly.
    """
    if car is None or car.fuelType is None or car.tareWeight is None or car.fuelTankCapacity is None:
        return None


    fuelMass = getFuelMass(car.fuelType, car.fuelTankCapacity / 2)
    if fuelMass is not None:
        return car.tareWeight + DRIVER_MASS + fuelMass
    else:
        return None


def getFuelMass(type, litres, precision=0):
    """
    For a given type and volume of fuel, calculates the mass in kilograms. Results roudned to
    nearest integer unless a precision is set.
    :param type:
    :param litres: [float] The amount of litres
    :param precision: [int] How many decimal places to round to (default 0)
    :return: [float] The mass, in kg, of the fuel, rounded to whatever precision requested
    """
    if type == constants.PETROL:
        mass = litres * PETROL_MASS_1L
    elif type == constants.DIESEL:
        mass = litres * DIESEL_MASS_1L
    elif type == constants.LPG:
        mass = litres * LPG_MASS_1L
    else:
        return None

    if precision is not None:
        return round(mass, precision)

def calculateCombinedFuelRating(car):
    """
    Will average out a urban and non urban fuel economy if
    :param car:
    :return:
    """
    cityEcon = findFirstMatching \
        (car.fuelEconomySet, [constants.URBAN, constants.CITY], constants.LITRES_PER_100_KM)
    nonCityEcon = findFirstMatching \
        (car.fuelEconomySet, [constants.EXTRA_URBAN, constants.HIGHWAY], constants.LITRES_PER_100_KM)
    if cityEcon is not None and nonCityEcon is not None:
        return (cityEcon.amount + nonCityEcon.amount) / 2
    else:
        return None