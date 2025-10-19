# My code is shit.
# Main file of YouBikePython.
import sys
import math
import requests
import argparse
from datetime import datetime


# thanks stackoverflow
def measure(lat1, lon1, lat2, lon2):
    R = 6378.137  # Radius of earth in KM
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dLon / 2) ** 2
         )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters


def getallstations(parkinginfo=True, gz=True):
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

    if parkinginfo:
        apiurl = 'https://apis.youbike.com.tw/json/station-yb2.json'
    else:
        apiurl = 'https://apis.youbike.com.tw/json/station-min-yb2.json'

    response = requests.get(
        apiurl,
        headers=headers
    )
    return response.json()


def getstationbyid(id, area_info=False, gz=True):
    stations = getallstations(gz=gz)
    for station in stations:
        if str(id) == station["station_no"]:
            if area_info:
                area = getareabyid(station["area_code"], gz=gz)
                station["area_info"] = area
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


def getstationbylocation(lat, lon, distance=0, data=None):
    # if distance is 0, get nearest station
    if distance < 0:
        raise Exception("Distance cannot < 0")
    if not data:
        data = getallstations()
    result = [] if distance > 0 else {}
    for station in data:
        td = measure(lat, lon, float(station["lat"]), float(station["lng"]))
        if distance > 0:
            if td <= distance:
                station["distance"] = td
                result.append(station)
        else:
            if result == {}:
                station["distance"] = td
                result = station
            elif td <= result["distance"]:
                station["distance"] = td
                result = station
    return result


def getallareas(gz=True):
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
        'https://apis.youbike.com.tw/json/area-all.json',
        headers=headers
    )
    return response.json()


def getareabyid(id: str, gz: bool = True):
    areas = getallareas(gz=gz)
    for area in areas:
        if str(id) == area["area_code"]:
            return area
    return None


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


class BikeStation:
    def __init__(self, station_data: dict):
        self.address_cn = station_data.get('address_cn')
        self.address_en = station_data.get('address_en')
        self.address_tw = station_data.get('address_tw')
        self.area_code = station_data.get('area_code')
        self.available_spaces = station_data.get('available_spaces')
        self.available_spaces_detail = station_data.get('available_spaces_detail')
        self.available_spaces_level = station_data.get('available_spaces_level')
        self.country_code = station_data.get('country_code')
        self.district_cn = station_data.get('district_cn')
        self.district_en = station_data.get('district_en')
        self.district_tw = station_data.get('district_tw')
        self.empty_spaces = station_data.get('empty_spaces')
        self.forbidden_spaces = station_data.get('forbidden_spaces')
        self.img = station_data.get('img')
        self.lat = station_data.get('lat')
        self.lng = station_data.get('lng')
        self.name_cn = station_data.get('name_cn')
        self.name_en = station_data.get('name_en')
        self.name_tw = station_data.get('name_tw')
        self.parking_spaces = station_data.get('parking_spaces')
        self.station_no = station_data.get('station_no')
        self.status = station_data.get('status')
        self.time = station_data.get('time')
        self.type = station_data.get('type')
        self.updated_at = datetime.strptime(station_data.get('updated_at'), '%Y-%m-%d %H:%M:%S') if station_data.get('updated_at') else None

    def __repr__(self):
        return f"<BikeStation {self.name_en} ({self.station_no})>",

    @classmethod
    def from_dict(cls, station_data):
        return cls(station_data)


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
