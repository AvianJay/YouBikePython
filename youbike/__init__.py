# My code is shit.
# Main file of YouBikePython.
import sys
import requests
import argparse


def getdata(gz=True):
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


def searchstation(name, data=None):
    if not data:
        data = getdata()
    results = []
    for station in data:
        if name in station["name_tw"]:
            results.append(station)
        elif name in station["district_tw"]:
            results.append(station)
        elif name in station["address_tw"]:
            results.append(station)
    return results


def formatdata(stations):
    result = "ID  名稱  總共車位  可停車位  YB2.0  YB2.0E\n"
    for station in stations:
        result += (
            f"{station['station_no']}  {station['name_tw']}  "
            f"{station['parking_spaces']}  {station['available_spaces']}  "
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
    args = parser.parse_args()

    if args.cmd == "showall":
        print(formatdata(getdata()))
    elif args.cmd == "search":
        print(formatdata(searchstation(args.name)))
    else:
        print("使用", sys.argv[0], "-h 來取得指令用法。")
        sys.exit(1)
