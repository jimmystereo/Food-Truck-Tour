import pandas as pd
from datetime import datetime
import googlemaps
import json

with open('tokens.json') as f:
    data = json.load(f)
    GOOGLE_API_KEY = data['GOOGLE_API_KEY']
    MAP_TOKEN = data['MAP_TOKEN']
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
df = pd.read_csv('../data/directions_driving.csv')

df2 = df.copy()

start = "Pico de Gallo Food Truck"
tour = [start]
for i in range(5):
    df_tmp = df2[df2['origin'] == start].sort_values(by="duration", ascending=True).reset_index(drop=True).iloc[0]
    print(df_tmp["destination"])
    start = df_tmp["destination"]
    tour.append(start)
    df2 = df2.where(df2['destination'] != start)


def get_route_between(origin, destination):
    now = datetime.now()

    directions_result = gmaps.directions({'lat': origin['lat'],
                                          'lng': origin['lng']}
                                         ,
                                         {'lat': destination['lat'],
                                          'lng': destination['lng']}
                                         ,
                                         mode="driving",
                                         departure_time=now)
    lats = []
    lngs = []
    for i in directions_result[0]['legs'][0]['steps']:
        lats.append(i['start_location']['lat'])

        lats.append(i['end_location']['lat'])
        lngs.append(i['start_location']['lng'])

        lngs.append(i['end_location']['lng'])
    return lats, lngs

df_detail = pd.read_csv('../data/food_trucks.csv')

lats = []
lngs = []
for i in range(len(tour)):
    if i == len(tour)-1:
        break
    origin = df_detail[df_detail['name']==tour[i]]
    destination = df_detail[df_detail['name']==tour[i+1]]
    lat, lng = get_route_between(origin, destination)
    lats = lats + lat
    lngs = lngs + lng
print(lats)
print(lngs)
