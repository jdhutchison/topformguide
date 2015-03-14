from topformguide.util import constants

"""Unit conversion helpers - especially metric to imperial and vice versa"""

# Conversion constants
MILES_TO_KILOMETRES = 1.609344
US_GALLLONS_TO_LITRES = 3.7854117891320316
CM3_IN_LITRE = 1000
HORSEPOWER_TO_KILLOWATTS = 0.745699872  # Mechanical horsepower
POUNDS_TO_KILOGRAMS = 0.453592
INCHES_TO_MILLIMETRES = 25.4
CUBIC_FEET_TO_LITRES = 28.3168
MILES_TO_KILOMETRES = 1.60934
POUNDS_FEET_TO_NEWTON_METRES = 1.35581795
NEWTON_METRES_TO_POUNDS_FEET = 0.73756214837

# Any sort of conversion
def genericConversionFunction(amount, conversionFactor, precision):
    """
    Performs a conversion of some sort by multiplying an amount by a factor and
    then rounding the result to a specific precision level.
    :param amount: [float] the number to convert
    :param conversionFactor: [float] what to multiply the amount by to convert
    :param precision: [int] how many decimal places
    :return: [float] The converted amount, with the precision requested, if any
    """
    if amount is None or conversionFactor is None:
        return None

    newAmount = amount * conversionFactor
    if precision is not None and precision >= 0:
        newAmount = round(newAmount, precision)

    return newAmount


# VOLUME CONVERSIONS
def usGallonsToLitres(gallons, precision=2):
    return genericConversionFunction(gallons, US_GALLLONS_TO_LITRES, precision)


def litresToCubicCm(litres):
    return litres * CM3_IN_LITRE;


def cubicCmToLitres(cm3, precision=1):
    return genericConversionFunction(cm3, 1.0 / CM3_IN_LITRE, precision)


def cubicFeetToLitres(cubicFeet, precision):
    return genericConversionFunction(cubicFeet, CUBIC_FEET_TO_LITRES, precision)


def convertVolumeToLitres(amount, unit, precision=2):
    """
    Converts any measure of volume to litres.
    :param amount: [int] the amount of the volume measurement
    :param unit: [string] what the volume is measured in - one of LITRES, GALLONS, CUBIC_CM
    :param precision: [int] the precision (amount of decimal places) for the returned value. Defaults to 2
    :return: the volume as measured in litres.
    """
    if amount is None:
        return None
    elif unit == constants.LITRES:
        return round(amount, precision)
    elif unit == constants.GALLONS:
        return usGallonsToLitres(amount, precision)
    elif unit == constants.CUBIC_CM:
        return cubicCmToLitres(amount)
    elif unit == constants.CUBIC_FEET:
        return cubicFeetToLitres(amount, precision)
    else:
        return None


# POWER CONVERSIONS
def convertHorsepowerToKillowatts(amount, precision=2):
    """
    Converts an amount in (mechanical) Horsepower to killowatts
    :param amount: [float] the number of horsepower
    :param precision: [int] how many decimal places to round the result off to.
    No rounding if set to None or -ve. Defaults to 2
    :return: [float] the amount in killowats, rounded if precision specified
    """
    kw = amount * HORSEPOWER_TO_KILLOWATTS
    if precision is not None and precision >= 0:
        kw = round(kw, precision)

    return kw


def convertPowerToKilloWatts(amount, unit):
    if amount is None:
        return None
    elif unit == constants.KILLOWATT:
        return amount
    elif unit == constants.HORSEPOWER:
        return convertHorsepowerToKillowatts(amount)
    else:
        return None


# FORCE CONVERSIONS
def poundsFeetToNewtonMetres(lbFt, precision=2):
    return genericConversionFunction(lbFt, POUNDS_FEET_TO_NEWTON_METRES, precision)


def newtonMetresToPoundsFeet(nm, precision=2):
    return genericConversionFunction(nm, NEWTON_METRES_TO_POUNDS_FEET, precision)


# MASS CONVERSIONS
def convertMassToKilograms(weight, unit, precision=2):
    """
    Converts a weight in some units to kilograms.

    :param weight: [float] the weight in whatever units
    :param unit: [string] what the weight is defined in - one of LB, KG
    :param precision: [int] how many decimal places to have (default 2). No rounding if None or -ve
    :return: [float] the mass converted to kilograms, rounded to the requested precision
    """

    if weight is None:
        return None
    elif unit == constants.KILOGRAMS:
        kg = weight
    elif unit == constants.POUNDS:
        kg = weight * POUNDS_TO_KILOGRAMS
    else:
        return None

    if precision is not None and precision >= 0:
        kg = round(kg, precision)

    return kg


# LENGTH/DISTANCE CONVERSIONS
def milesToKilometres(miles, precision=2):
    """
    Converts an amount in miles to the equivalent in kilometres
    :param miles: [float] how many miles to convert.
    :param precision: [int] The number of decimal places to round to (default is 2). No rounding if this is None or -ve
    :return: the number of kilometres, rounded to the precision specified
    """
    return genericConversionFunction(miles, MILES_TO_KILOMETRES, precision)


def convertLengthToMillimetres(length, unit, precision=1):
    """
    Converts a length in an arbitrary unit to millimetres.

    :param length: [float] the amount of the length
    :param unit: what the length is defined in - one of mm, cm, inches (case insensitive, e.g. mm == MM = mM)
    :param precision: [int] how many decimal places to have (default 1). No rounding if None or -ve
    :return: [float] the length, converted to millimetres, at the required precision
    """
    # Force unit to lower case
    unit = unit.lower()

    if length is None:
        return None
    elif unit == constants.MILLIMETRES:
        mm = length
    elif unit == constants.CENTIMETRES:
        mm = length * 10
    elif unit == constants.INCHES:
        mm = length * INCHES_TO_MILLIMETRES
    else:
        return None

    if precision is not None and precision >= 0:
        mm = round(mm, precision)

    return mm


def convertDistanceToKilometres(amount, unit, precision=2):
    if amount is None:
        return None
    elif unit == constants.MILES:
        return genericConversionFunction(amount, MILES_TO_KILOMETRES, precision)
    elif unit == constants.KILOMETRES:
        return genericConversionFunction(amount, 1, precision)
    else:
        return None


# FUEL EFFICIENCY
def mpgToLitresPer100km(mpg, precision=1):
    """
    Converts a measurement of miles per gallon into an equivalent litres to 100km.

    :param mpg: [float] the miles per gallon
    :param precision: [int] how many decimal places to have (default 1). No rounding if None or -ve
    :return: [float] The converted efficency with the requested precision
    """

    # How many gallons to get 100km?
    gallonsTo100km = 100 / milesToKilometres(mpg, None)
    litresTo100km = usGallonsToLitres(gallonsTo100km, None)

    if precision is not None:
        litresTo100km = round(litresTo100km, precision)

    return litresTo100km
