import googlemaps
import pickle
import pandas as pd
from datetime import datetime


def save_object(target, path):
    pickle.dump(target, open(path, 'w'))


import json

with open('tokens.json') as f:
    data = json.load(f)
    GOOGLE_API_KEY = data['GOOGLE_API_KEY']
    MAP_TOKEN = data['MAP_TOKEN']
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

techpoint = {
    "location": {
        'lat': 39.78728396765869,
        'lng': -86.18316063589883}
}

## Get data
trucks_raw = gmaps.places_nearby(location=techpoint['location'], radius=10000, keyword='food truck')

number_of_trucks = len(trucks_raw['results'])

df_json = []
details = []


def try_get_data(return_json, key):
    if key == 'reviews':
        try:
            result = len(return_json["reviews"])
        except:
            result = 0
    else:
        try:
            result = return_json[key]
        except:
            result = None
    return result


for i in trucks_raw['results']:
    place_details = gmaps.place(i['place_id'])
    details_results = place_details.get('result')
    details.append(details_results)
    json_truck = {'name': i['name'],
            'rating': i['rating'],
            'lat': i['geometry']['location']['lat'],
            'lng': i['geometry']['location']['lng'],
            'address':
                details_results['adr_address'].replace('<span class="street-address">', '').strip("'").split(
                    '</span>')[0],
            'url': details_results['url']}
    json_truck['serves_beer'] = try_get_data(details_results, 'serves_beer')
    json_truck['serves_dinner'] = try_get_data(details_results, 'serves_dinner')

    json_truck['serves_lunch'] = try_get_data(details_results, 'serves_lunch')
    json_truck['serves_wine'] = try_get_data(details_results, 'serves_wine')
    json_truck['takeout'] = try_get_data(details_results, 'takeout')
    json_truck['dine_in'] = try_get_data(details_results, 'dine_in')

    json_truck['reviews'] = try_get_data(details_results, 'reviews')

    df_json.append(json_truck)

df = pd.DataFrame(df_json, index=[i for i in range(len(df_json))])

df.to_csv("food_trucks.csv", encoding='utf-8-sig', index=False)

distance_json = []
mode = 'driving'
for i in range(len(trucks_raw['results'])):
    for j in range(len(trucks_raw['results'])):
        if i == j:
            continue
        now = datetime.now()
        try:
            directions_result = gmaps.directions({'lat': trucks_raw['results'][i]['geometry']['location']['lat'],
                                                  'lng': trucks_raw['results'][i]['geometry']['location']['lng']}
                                                 ,
                                                 {'lat': trucks_raw['results'][j]['geometry']['location']['lat'],
                                                  'lng': trucks_raw['results'][j]['geometry']['location']['lng']}
                                                 ,
                                                 mode=mode,
                                                 departure_time=now)
        except:
            print(trucks_raw['results'][i]['name'], trucks_raw['results'][j]['name'])
            tmp_json = {}
            tmp_json['i'] = i
            tmp_json['j'] = j
            tmp_json['origin'] = trucks_raw['results'][i]['name']
            tmp_json['destination'] = trucks_raw['results'][j]['name']

            tmp_json['distance'] = None
            tmp_json['duration'] = None
            distance_json.append(tmp_json)
            continue
        tmp_json = {}
        tmp_json['i'] = i
        tmp_json['j'] = j
        tmp_json['origin'] = trucks_raw['results'][i]['name']
        tmp_json['destination'] = trucks_raw['results'][j]['name']

        tmp_json['distance'] = directions_result[0]['legs'][0]['distance']['value']
        tmp_json['duration'] = directions_result[0]['legs'][0]['duration']['value']
        tmp_json['lats'] = []
        tmp_json['lngs'] = []
        for k in directions_result[0]['legs'][0]['steps']:
            tmp_json['lats'] .append(k['start_location']['lat'])

            tmp_json['lats'] .append(k['end_location']['lat'])
            tmp_json['lngs'].append(k['start_location']['lng'])

            tmp_json['lngs'].append(k['end_location']['lng'])


            distance_json.append(tmp_json)
# Serializing json
json_object = json.dumps(distance_json, indent=4)

# Writing to sample.json
with open("../data/full_data.json", "w") as outfile:
    outfile.write(json_object)


df2 = pd.DataFrame(distance_json, index=[i for i in range(len(distance_json))])

df2.to_csv("directions_driving.csv", encoding='utf-8-sig', index=False)




now = datetime.now()

directions_result = gmaps.directions({'lat': trucks_raw['results'][1]['geometry']['location']['lat'],
                                      'lng': trucks_raw['results'][1]['geometry']['location']['lng']}
                                     ,
                                     {'lat': trucks_raw['results'][2]['geometry']['location']['lat'],
                                      'lng': trucks_raw['results'][2]['geometry']['location']['lng']}
                                     ,
                                     mode="transit",
                                     departure_time=now)

