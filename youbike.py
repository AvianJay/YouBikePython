import json
import requests

def getdata():
    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Accept-Encoding': 'gzip',
        'content-encoding': 'gzip',
    }

    response = requests.get('https://apis.youbike.com.tw/json/station-yb2.json', headers=headers)
    return response.json()

def searchstation(name, data=getdata()):
    results = []
    for station in data:
        if name in station["name_tw"]:
            results.append(station)
        elif name in station["district_tw"]:
            results.append(station)
        elif name in station["address_tw"]:
            results.append(station)
    return results