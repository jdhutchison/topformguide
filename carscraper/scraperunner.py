from scrapers.carsales import CarSalesScraper
import json
import sys
import traceback

jsonFile = open('carsales-AU-data.json', 'w')
writeFunction = lambda car: jsonFile.write(json.dumps(car.__dict__, default=lambda o: o.__dict__) + '\n')

scraper = CarSalesScraper()
scraper.postCarFunction = writeFunction

try:
    scraper.getCarData()
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)

print('Total number of cars parsed: %d' % len(scraper.cars))

# Write to disk
# jsonFile = open('carsales-AU-data.json', 'w')
#for car in scraper.cars:
#    jsonFile.write(json.dumps(car.__dict__, default=lambda o: o.__dict__) + '\n')
jsonFile.close()