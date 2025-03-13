# My code is shit.
# Main file of YouBikePython.
import sys
import math
import requests
import argparse


# thanks stackoverflow
def measure(lat1, lon1, lat2, lon2):
    R = 6378.137  # Radius of earth in KM
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters


def getallstations(gz=True):
    if gz:
        headers = {
            'User-Agent': 'Dart/3.3 (dart:io)',
            'Accept-Encoding': 'gzip',
            'content-encoding': 'gzip',
        }
    else:
        headers = {
            'User-Agent': 'Dart/3.3 (dart:io)',
        }

    response = requests.get(
        'https://apis.youbike.com.tw/json/station-yb2.json',
        headers=headers
    )
    return response.json()


def getstationbyid(id, gz=True):
    stations = getallstations(gz=gz)
    for station in stations:
        if id == station["station_no"]:
            return station
    return None


def getstationbyname(name, data=None):
    if not data:
        data = getallstations()
    results = []
    for station in data:
        if name in station["name_tw"]:
            results.append(station)
        elif name in station["district_tw"]:
            results.append(station)
        elif name in station["address_tw"]:
            results.append(station)
    return results


def getstationbylocation(lat, lon, distance, data=None):
    if not data:
        data = getallstations()
    results = []
    for station in data:
        td = measure(lat, lon, float(station["lat"]), float(station["lng"]))
        if td<=distance:
            results.append(station)
    return results


def formatdata(stations):
    result = "ID  名稱  總共車位  可停車位  YB2.0  YB2.0E\n"
    for station in stations:
        # I don't know why their api available is parked
        available = station['parking_spaces'] - station['available_spaces']
        result += (
            f"{station['station_no']}  {station['name_tw']}  "
            f"{station['parking_spaces']}  {available}  "
            f"{station['available_spaces_detail']['yb2']}  "
            f"{station['available_spaces_detail']['eyb']}\n"
        )
    return result


def main():
    parser = argparse.ArgumentParser(description="YouBike API for Python")
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.add_parser("showall", help="取得所有站點資料（不建議）")
    parser_search = subparsers.add_parser("search", help="搜尋站點")
    parser_search.add_argument("name", help="關鍵字", type=str)
    parser_location = subparsers.add_parser("location", help="利用座標取得站點")
    parser_location.add_argument("lat", help="緯度", type=float)
    parser_location.add_argument("lon", help="經度", type=float)
    parser_location.add_argument("distance", help="距離(公尺)", type=float)
    args = parser.parse_args()

    if args.cmd == "showall":
        print(formatdata(getallstations()))
    elif args.cmd == "search":
        print(formatdata(getstationbyname(args.name)))
    elif args.cmd == "location":
        print(formatdata(getstationbylocation(
            args.lat,
            args.lon,
            args.distance)))
    else:
        print("使用", sys.argv[0], "-h 來取得指令用法。")
        sys.exit(1)
