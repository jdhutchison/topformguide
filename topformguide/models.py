from django.db import models

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

class AlternateName(models.Model):
    make = models.ForeignKey(Make, related_name='alternateNames')
    name = models.CharField(max_length=64)

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
        ('ULP', 'Unleaded petrol'),
        ('DIESEL', 'Diesel'),
        ('LPG', 'Natural NPG'),
        ('ELECTRICITY', 'Electric')
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
        ('STATION_WAGON', 'Station Wagon'),
        ('UTE', 'Utility'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('SPORTS', 'Sports'),
        ('SUV', 'SUV'),
        ('PEOPLE_MOVER', 'People Mover')
    )

    TRANSMISSION_TYPES = (
        ('AUTO', 'Automatic'),
        ('MANUAL', 'Manual')
    )

    DRIVE_TYPE = (
        ('REAR', 'Rear wheel drive'),
        ('FRONT', 'Front wheel drive'),
        ('ALL', 'All wheel drive'),
        ('4WD', 'Four wheel drive')
    )

    # Key details
    model = models.ForeignKey(CarModel, related_name='models')
    name = models.CharField('The name of the variant - this may be just the year', max_length=64)
    year = models.IntegerField('The year of the variant')
    countries = models.ManyToManyField(Country)
    doors = models.IntegerField('The number of doors')
    seats = models.IntegerField('Maximum seating capacity')

    # Engine details
    torque = models.OneToOneField(PowerRating, null=True)
    engineType = models.CharField('The type of engine', choices=ENGINE_TYPE, max_length=16)
    cylinders = models.IntegerField('How many cylinders for a combustion engine', null=True)

    # Transmission
    transmission = models.CharField('The type of transmission: auto or manual', choices=TRANSMISSION_TYPES, max_length=10)
    speeds = models.IntegerField('The number of speeds/gears')

    # Fuel and emission details
    fuelType = models.CharField('The type of fuel consummed', choices=FUEL_TYPES, max_length=8)
    fuelTankCapacity = models.IntegerField('Capacity of fuel tank in litres')
    emissions = models.FloatField('Grams of CO2 emitted per kg', null=True)
    eGoRating = models.IntegerField('E-Go rating', null=True)

    # Performance
    topSpeedInKph = models.FloatField('Max speed of car in km/h')
    topSpeedInMph = models.FloatField('Max speed of car in mph', null=True)
    zeroTo100Kph = models.FloatField('Time (in seconds) from 0kph to 100kph')
    zeroTo60mph = models.FloatField('Time (in seconds) from 0mph to 60mph', null=True)

    # Body and size
    body = models.CharField("The Body type of the car", choices=BODY_TYPES, max_length=16)

    kerbWeight = models.FloatField("The Kerb Weight of the care (in kg)")
    grossWeight = models.FloatField('The gross mass of the vehicle', null=True)
    tareWeight = models.FloatField('The tared mass of the vehicle', null=True)

    wheelbase = models.IntegerField('Width between the wheels in mm')
    length = models.IntegerField('The length of the car in mm')
    width = models.IntegerField('Maximum width of the body in mm')
    interiorVolume = models.FloatField('How much interior space the car has in cubic cm', null=True)
    bootVolume = models.FloatField('How much interior space the boot of the car has in cubic cm', null=True)

    # Safety details
    safetyRating = models.FloatField('The safety rating of the car', null=True)
    safetyRatingSource = models.CharField('Who produced the safety rating', null=True, max_length=16)

    created = models.DateTimeField("When the Make was first created")#, default=)
    lastUpdated = models.DateTimeField("When the Make was last updated")
    deleted = models.BooleanField('Is the Make logically deleted?', default=False)

class FuelEconomy(models.Model):
    """Records different types of fuel economy"""
    # How the fuel economy is expressed
    ECONOMY_TYPES = (
        ('L100KM', 'Litres per 100km'),
        ('MPG', 'Miles per Gallon (US)')
    )

    # What the fuel conomny
    CONDITION = (
        ('URBAN', 'Urban driving (US)'),
        ('HIGHWAY', 'Highway driving (US)'),
        ('CITY', 'City driving (AUS)'),
        ('NONCITY', 'Non-city/Highway/Rural driving (AUS)'),
        ('COMBINED', 'Combined/average/typical usage')
    )

    vairant = models.ForeignKey(Variant, related_name='fuelEcomonySet')
    amount = models.FloatField("How efficient in either MPG or L/100km")
    unit = models.CharField("The econ rating unit measurement - l/100km or MPG", choices= ECONOMY_TYPES, max_length=10)
    condition = models.CharField("What type of driving this rating applies to", choices=CONDITION, max_length=10)

class EnginePower(PowerRating):
    UNIT = (
        ('kW', 'KilloWatts'),
        ('KJ', 'Killojoule'),
        ('HP', 'Horsepower')
    )
    variant = models.ForeignKey(Variant, related_name='enginePowerSet')
    unit = models.CharField('The power unit for this rating', choices=UNIT, max_length=2);


class RawData(models.Model):
    """"The data scraped from a source """
    vairant = models.ForeignKey(Variant, related_name='rawDataRecords')
    data = models.TextField("The raw JSON/XML as scraped")
    fecthDate = models.DateTimeField("When the data was fetched/scraped")
    source = models.TextField("Wher the data came from", max_length=255)
    pass