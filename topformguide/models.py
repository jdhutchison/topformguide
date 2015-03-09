from django.db import models

from util import constants


class Country(models.Model):
    """Represents a physical nation state"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name="2 letter ISO country code")
    name = models.CharField(max_length=32, verbose_name="Common English name for the country")

class Make(models.Model):
    """A car manufacturer"""
    name = models.CharField(max_length=64, unique=True, verbose_name="Common name of Manufacturer")
    country = models.ForeignKey(Country, verbose_name="Home country of manufacturer", null=True)
    created = models.DateTimeField("When the Make was first created")#, default=)
    lastUpdated = models.DateTimeField("When the Make was last updated")
    deleted = models.BooleanField('Is the Make logically deleted?', default=False)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return self.__str__()


# class AlternateName(models.Model):
#    make = models.ForeignKey(Make, related_name='alternateNames')
#    name = models.CharField(max_length=64)

class CarModel(models.Model):
    make = models.ForeignKey(Make, related_name='models')
    name = models.CharField(max_length=64)
    year = models.IntegerField('The year of the variant')
    country = models.ForeignKey(Country, verbose_name="Country where Model is sold", null=True, related_name='models')
    created = models.DateTimeField("When the Make was first created")#, default=)
    lastUpdated = models.DateTimeField("When the Make was last updated")
    deleted = models.BooleanField('Is the Make logically deleted?', default=False)

class PowerRating(models.Model):
    """Meansures how powerful the engine is"""
    power = models.FloatField('The ammount of power')
    minRpm = models.IntegerField('How many RPMs for this rating', null = True)
    maxRpm = models.IntegerField('Maximum RPMs for this rating', null = True)

class Variant(models.Model):
    """"A model of a ca """
    FUEL_TYPES = (
        (constants.PETROL, 'Unleaded petrol'),
        (constants.DIESEL, 'Diesel'),
        (constants.LPG, 'Natural NPG'),
        (constants.ELECTRIC, 'Electric')
    )

    ENGINE_TYPE = (
        ('PISTON', 'Piston'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid engine'),
        ('COMBUSTION', 'Internal Combustion')
    )

    BODY_TYPES = (
        ('SEDAN', 'Sedan'),
        ('HATCHBACK', 'Hatchback'),
        ('WAGON', 'Station Wagon'),
        ('UTE', 'Utility'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('SPORTS', 'Sports'),
        ('SUV', 'SUV'),
        ('PEOPLE_MOVER', 'People Mover'),
        ('CAB_CHASSIS', 'Cab Chassis'),
        ('LIGHT_TRUCK', 'Light Truck')
    )

    TRANSMISSION_TYPES = (
        ('AUTO', 'Automatic'),
        ('MANUAL', 'Manual'),
        ('SPORT', 'Sports transmission')
    )

    DRIVE_TYPE = (
        (constants.REAR, 'Rear wheel drive'),
        (constants.FRONT, 'Front wheel drive'),
        (constants.ALL_WHEEL_DRIVE, 'All wheel drive'),
        (constants.FOUR_BY_FOUR, 'Four wheel drive')
    )

    # Key details
    model = models.ForeignKey(CarModel, related_name='models')
    name = models.CharField('The name of the variant - this may be just the year', max_length=64)
    year = models.IntegerField('The year of the variant', null=True)
    countries = models.ManyToManyField(Country)
    doors = models.IntegerField('The number of doors')
    seats = models.IntegerField('Maximum seating capacity')
    driveType = models.CharField('The type of drive(train)', choices=DRIVE_TYPE, max_length=8)

    # Engine details
    torque = models.FloatField('The engine torque in Nm', null=True)
    torqueRpms = models.IntegerField('At what RPMs the engine produces the torque', null=True)
    torqueRpmsHigh = models.IntegerField('Upper limit of RPMs the engine produces the torque', null=True)
    engineType = models.CharField('The type of engine', choices=ENGINE_TYPE, max_length=16)
    cylinders = models.IntegerField('How many cylinders for a combustion engine', null=True)
    enginePower = models.FloatField('The engine power in kW', null=True)
    enginePowerRpms = models.IntegerField('At what RPMs the engine produces the power', null=True)
    enginePowerRpmsHigh = models.IntegerField('At what RPMs the engine produces the power', null=True)

    # Transmission
    transmission = models.CharField('The type of transmission: auto or manual', choices=TRANSMISSION_TYPES, max_length=10)
    speeds = models.IntegerField('The number of speeds/gears')

    # Fuel and emission details
    fuelType = models.CharField('The type of fuel consummed', choices=FUEL_TYPES, max_length=8)
    fuelTankCapacity = models.IntegerField('Capacity of fuel tank in litres')
    fuelRange = models.IntegerField('How far the car can go in mk', null=True)
    standardEmissions = models.FloatField('Grams of CO2 emitted per kg', null=True)
    eGoRating = models.IntegerField('E-Go rating', null=True)

    # Performance
    topSpeed = models.FloatField('Max speed of car in km/h')
    zeroTo100Kph = models.FloatField('Time (in seconds) from 0kph to 100kph', null=True)
    zeroTo60mph = models.FloatField('Time (in seconds) from 0mph to 60mph', null=True)

    # Body and size
    body = models.CharField("The Body type of the car", choices=BODY_TYPES, max_length=16)

    kerbWeight = models.FloatField("The Kerb Weight of the care (in kg)", null=True)
    grossWeight = models.FloatField('The gross mass of the vehicle', null=True)
    tareWeight = models.FloatField('The tared mass of the vehicle', null=True)
    payload = models.FloatField('Maximum weight the car can carr (in kg)', null=True)
    kerbWeightCalculated = models.BooleanField("Was kerb data scraped or calcualted?", default=False)

    wheelbase = models.IntegerField('Width between the wheels in mm')
    length = models.IntegerField('The length of the car in mm')
    width = models.IntegerField('Maximum width of the body in mm')
    interiorVolume = models.FloatField('How much interior space the car has in litres', null=True)
    bootVolume = models.FloatField('How much interior space the boot of the car has in litres', null=True)

    # Safety details
    safetyRating = models.FloatField('The safety rating of the car', null=True)
    safetyRatingSource = models.CharField('Who produced the safety rating', null=True, max_length=16)
    airbags = models.IntegerField('How many airbags the car has', null=True)

    created = models.DateTimeField("When the Make was first created")#, default=)
    lastUpdated = models.DateTimeField("When the Make was last updated")
    deleted = models.BooleanField('Is the Make logically deleted?', default=False)

class FuelEconomy(models.Model):
    """Records different types of fuel economy"""
    # How the fuel economy is expressed
    ECONOMY_TYPES = (
        (constants.LITRES_PER_100_KM, 'Litres per 100km'),
        (constants.MILES_PER_GALLON, 'Miles per Gallon (US)')
    )

    # What the fuel conomny
    CONDITION = (
        (constants.URBAN, 'Urban driving'),
        (constants.CITY, 'City driving (US)'),
        (constants.HIGHWAY, 'Highway driving (US)'),
        (constants.EXTRA_URBAN, 'Non city driving (AUS)'),
        (constants.COMBINED, 'Combined/average/typical usage')
    )

    vairant = models.ForeignKey(Variant, related_name='fuelEcomonySet')
    amount = models.FloatField("How efficient in either MPG or L/100km")
    unit = models.CharField("The econ rating unit measurement - l/100km or MPG", choices= ECONOMY_TYPES, max_length=10)
    condition = models.CharField("What type of driving this rating applies to", choices=CONDITION, max_length=10)
    calculated = models.BooleanField("Was this emission data scraped or calcualted?", default=False)

class EmissionData(models.Model):
    """Tracks an emission level under a given driving condition"""
    variant = models.ForeignKey(Variant, related_name='emissionDataSet')
    amount = models.FloatField("How much CO2 per kilometre the car emits")
    condition = models.CharField("What type of driving this rating applies to", choices=FuelEconomy.CONDITION, max_length=10)
    calculated = models.BooleanField("Was this emission data scraped or calcualted?", default=False)

class RawData(models.Model):
    """"The data scraped from a source """
    variant = models.ForeignKey(Variant, related_name='rawDataRecords')
    data = models.TextField("The raw JSON/XML as scraped")
    fetchDate = models.DateTimeField("When the data was fetched/scraped")
    source = models.TextField("Where the data came from", max_length=255)