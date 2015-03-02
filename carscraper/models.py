class CarData:
    def __init__(self):
        self.make = None
        self.model = None
        self.variant = None
        self.year = 0
        self.country = None # 2 letter ISO country code - upper case
        self.doors = 0
        self.seats = 0
        self.enginePower = None # Optional, PowerRating
        self.engineType = None # One of 'ELECTRIC', 'COMBUSTION', 'PISTON', 'HYBRID'
        self.engineCylinders = 0
        self.torque = None # Optional, PowerRating
        self.transmission = None # One of 'AUTO', 'MANUAL'
        self.transmissionSpeeds = 0
        self.fuelConsumption = []
        self.fuelType = None # One of 'ELECTRIC', 'PETROL', 'LPG'. 'ULP' should be converted to PETROL
        self.fuelTank = 0 # Capacity of Fuel take, regardless of unit
        self.fuelTankUnit = None # One of LITRES, kW, GALLONS
        self.emissions = None
        self.emissionsUnit = None # One of Co2/KG...
        self.topSpeed = None
        self.topSpeedUnit = None # One of KPH, MPH
        self.secondsTo = 0 # How many seconds to get to some speed, ie. 100kmh/60mph
        self.secondsToSpeed = None # The speed for above - should be one of '100KPH' or '60MPH'
        self.bodyType = None # One of 'SEDAN', 'STATION_WAGON', 'HATCHBACK', 'COUPE', 'CONVERTIBLE', 'UTE', 'PEOPLE_MOVER', 'SUV', 'VAN'
        self.kerbWeight = 0 # Mandatory, integer
        self.grossWeight = 0 # Optional, integer
        self.tareWeight = 0 # Optional, integer
        self.weightUnit = None # Mandatory, string - One of 'KG', 'LBS'
        self.wheelbase = None # Mandatory, integer
        self.length = None # Mandatory, integer
        self.width = None # Optional, integer
        self.sizeUnits # Mandatory, string - what unit the sie measurements of the car are in. One of 'MM', 'INCHES'
        self.interiorVolume = None # Optional, integer
        self.bootVolume = None # Optional, integer
        self.safetyRating = 0 # Optional, float
        self.safetyRatingSource = None # Optional, string
        self.sourceUrl = None # Mandatory, url - The URL the data was scraped/obtained from
        self.timestamp = None # Mandatory, datetime - When the data was scraped or obtained

class PowerRating:
    def __init__(self):
        self.power = 0 # Mandatory, integer
        self.unit = None # Mandatory, string - The unit for the pwoer amount above. One of 'kW', 'HP', 'Nm'
        self.rpmLower = None # Optional, integer - amount, or lower amount if a range, of RPM needed to get above power
        self.rpmUpper = None # Optional, integer - upper amount of RPMs needed to obtain above power

class FuelEconomy:
    def __init__(self):
        self.economy = 0 # Mandatory, float/integer - How much 'mileage' the economy rating is for
        self.unit = None # Mandatory, string - the unit of this rating. One of 'MPG', 'L100KM'
        self.type = None # Mandatory, string - the type of driving the economy is for. One of 'URBAN'. 'HIGHWAY', 'CITY', 'EXTRACITY', 'RURAL', 'COMBINED', 'AVERAGE'



