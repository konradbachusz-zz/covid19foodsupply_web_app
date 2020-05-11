import pgeocode
import csv
import geopy
import time

MAPBOX_APIKEY = ''

## better precision using mapbox but incomplete data should be expected and API limitation per month for free tier
def convertByMapbox(postcode):
    geocoder = geopy.MapBox(api_key=MAPBOX_APIKEY)
    location = geocoder.geocode(postcode, timeout=30)
    lat = 0
    lon = 0
    if location:
        lat = geocoder.geocode(postcode).latitude
        lon = geocoder.geocode(postcode).longitude
    else:
        lat, lon = convertPostcodeToCoordinates(postcode, 'gb')
    return lat, lon

## set geocoder function, area/munacipal precision
def convertPostcodeToCoordinates(postcode, country):
    nomi = pgeocode.Nominatim('gb')
    location = nomi.query_postal_code(postcode)
    return location['latitude'], location['longitude']

list_data = list()
with open('supermarkets_v2.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    counter = 0
    for row in reader:
        # uncomment this if you get API limit restriction
        # if counter > 199 and counter < 500:
        lat, lon = convertByMapbox(row[0])
        # row.extend([lat, lon])
        data = {
            'postcodes': row[0],
            'latitude': lat,
            'longitude': lon
        }
        list_data.append(data)
        counter += 1
        print(counter)

with open('supermarkets_v2_1.csv', 'w') as writeFile:
    writer = csv.DictWriter(writeFile, fieldnames = ["postcodes", "latitude", "longitude"])
    writer.writerows(list_data)

csvFile.close()
writeFile.close()
