#!/usr/bin/python

import requests
import argparse
import json
import csv
import sys

class CieloTest:
   # def __init__(self):
        #self.session = requests.session()

    def get(self, url, save=False, filename='test', ext='json'):
        items = ''
        r = requests.get(url)

        if r.status_code == 200:
            result = r.json()

            if save:
                filename = filename + '.' + ext
                if ext == 'json':

                    with open(filename, 'w') as outfile:
                        json.dump(result, outfile)

                elif ext == 'csv':
                    f = csv.writer(open(filename, "wb+"))
                    f.writerow([
                        "body",
                        "userId",
                        "id",
                        "title"
                    ])

                    if len(result) > 0:
                        for item in result:
                            f.writerow([
                                item["body"],
                                item["userId"],
                                item["id"],
                                item["title"],
                            ])
        else:
            result = {
                "error": {
                    "code": 400,
                    "message": "Problems parsing JSON"
                  }
                }

        return result

    def post(self, url, save=False, data=None, filename='test', ext='json'):

        if save:
            filename = filename + '.' + ext
            if ext == 'json':
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile)
            else:
                headers = {'content-type': 'application/json'}

                r = requests.post(url, headers=headers, data=data)

                data = r.json()

                if result['status'] == 200:
                   data = data

        return data



if __name__ == '__main__':
    ces = CieloTest()
    parser = argparse.ArgumentParser()
    parser.add_argument("method", help="Request method", choices=['get','post'])
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--DATA", help="Data to send with request")
    parser.add_argument("-o", "--OUTPUT", help="Output to .json or .csv file")

    args = parser.parse_args()
    url = args.endpoint

    if args.method == 'get':

        if args.OUTPUT:
            file2save = args.OUTPUT
            ext = file2save.split('.')
            if ext[1] == 'json' or ext[1] == 'csv':
                result = ces.get(url, save=True, filename=ext[0], ext=ext[1])
                result = {
                    "status": 200,
                    "result": result
                }
            else:
                result = {
                    "status": 400,
                    "error": {
                        "code": 422,
                        "message": "file extension " + ext[1] + " is not allowed"
                    }
                }

            print json.dumps(result, indent=3)

        else:
            result = ces.get(url)
            result = {
                "status": 200,
                "result": result
            }
            temp = sys.stdout
            sys.stdout = open('log.txt', 'w')
            print json.dumps(result, indent=3)
            sys.stdout.close()
            sys.stdout = temp

            print json.dumps(result, indent=3)

    elif args.method == 'post':

        if args.DATA:
            data = args.DATA

        if args.OUTPUT:
            file2save = args.OUTPUT
            ext = file2save.split('.')

            result = ces.post(url=url, save=True, data=data, filename=ext[0], ext=ext[1])
            result = {
                "status": 200,
                "result": result
            }
        else:
            result = ces.post(url=url, data=data)
            result = {
                "status": 200,
                "result": result
            }

        print  result