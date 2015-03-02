__author__ = 'hutch'

#
MILES_TO_KILOMETRES = 1.609344
US_GALLLONS_TO_LITRES = 3.7854117891320316
CM3_IN_LITRE = 1000

def milesToKilometres(miles, precision = 2):
    kms = miles * MILES_TO_KILOMETRES
    if precision is not NONE and precision >= 0:
        kms = round(kms, precision)

    return kms

def usGallonsToLitres(gallons, precision = 2):
    litres = gallons * US_GALLLONS_TO_LITRES
    if precision is not NONE and precision >= 0:
        litres = round(litres, precision)

    return litres


def mpgToLitresPer100km(mpg, precision = 1):

    # How many gallons to get 100km?
    gallonsTo100km = 100 / milesToKilometres(mpg, NONE)
    litresTo100km = usGallonsToLitres(gallonsTo100km, NONE)

    if precision is not NONE:
        litresTo100km = round(litresTo100km, precision)

    return litresTo100km

def litresToCubicCm(litres):
    return litres * CM3_IN_LITRE;

def cubicCmToLitres(cm3, precision = 1):
    litres = cm3 / CM3_IN_LITRE

    if precision is not None and precision > 0:
        litres = round(litres, precision)

    return precision