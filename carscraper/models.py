class CarData:
    def __init__(self):
        self.make = None
        self.model = None
        self.variant = None
        self.year = None
        self.country = None # 2 letter ISO country code - upper case
        self.doors = None
        self.seats = None
        self.driveType = None # Mandatory, string one of 'REAR', 'FRONT', 'ALL', '4X4'
        self.engineVolume = None # Optional, float
        self.engineVolumeUnit = None # Optional, String - unit for above measurement. One of 'CC', 'LITRES', '???'
        self.enginePower = None # Optional, int - engine power in kw or hp
        self.enginePowerRpm = None # Optional, int
        self.enginePowerRpmHigh = None # Optional, int
        self.enginePowerUnit = None # Optional, string - unit for above. One of
        self.engineType = None # One of 'ELECTRIC', 'COMBUSTION', 'PISTON', 'HYBRID'
        self.engineCylinders = None
        self.torque = None # Optional, float
        self.torqueRpm = None # Optional, float - at what RPM the above torque mesurement is good for
        self.torqueRpmHigh = None
        self.transmission = None # One of 'AUTO', 'MANUAL'
        self.transmissionSpeeds = None
        self.fuelConsumption = []
        self.fuelType = None # One of 'ELECTRIC', 'PETROL', 'LPG'. 'ULP' should be converted to PETROL
        self.fuelTank = None # Capacity of Fuel take, regardless of unit
        self.fuelTankUnit = None # One of LITRES, kW, GALLONS
        self.fuelRange = None
        self.batteryRange = None
        self.rangeUnit = None  # Optional (mandatory is fuelRange set), String,
        self.emissions = []
        self.topSpeed = None
        self.topSpeedUnit = None # One of KPH, MPH
        self.secondsTo = None # How many seconds to get to some speed, ie. 100kmh/60mph
        self.secondsToUnit = None # The speed for above - should be one of '100KPH' or '60MPH'
        self.bodyType = None # One of 'SEDAN', 'WAGON', 'HATCHBACK', 'COUPE', 'CONVERTIBLE', 'UTE', 'PEOPLE_MOVER', 'SUV', 'VAN'
        self.kerbWeight = None # Mandatory, integer
        self.grossWeight = None # Optional, integer
        self.tareWeight = None # Optional, integer
        self.payload = None # Optional, integer
        self.weightUnit = None # Mandatory, string - One of 'KG', 'LBS'
        self.wheelbase = None # Mandatory, integer
        self.length = None # Mandatory, integer
        self.width = None # Optional, integer
        self.height = None
        self.lengthUnits = None # Mandatory, string - what unit the sie measurements of the car are in. One of 'MM', 'INCHES'
        self.interiorVolume = None # Optional, integer
        self.bootVolume = None # Optional, integer
        self.volumeUnit = None # Optional, string - what unit internal volume measured in
        self.safetyRating = None # Optional, float
        self.safetyRatingSource = None # Optional, string
        self.airbags = None # Optional,
        self.sourceUrl = None # Mandatory, url - The URL the data was scraped/obtained from
        self.timestamp = None # Mandatory, datetime - When the data was scraped or obtained

class FuelEconomy:
    def __init__(self):
        self.amount = None # Mandatory, float/integer - How much 'mileage' the economy rating is for
        self.unit = None # Mandatory, string - the unit of this rating. One of 'MPG', 'L100KM'
        self.type = None # Mandatory, string - the type of driving the economy is for. One of 'URBAN'. 'HIGHWAY', 'CITY', 'EXTRACITY', 'RURAL', 'COMBINED', 'AVERAGE'

class EmissionLevel:
    def __init__(self):
        self.amount = None
        self.unit = None
        self.type = None

