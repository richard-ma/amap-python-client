#!/usr/bin/env python
# encoding: utf-8

# URL example:
# http://restapi.amap.com/v3/direction/riding?origin=116.434307,39.90909&destination=116.434446,39.90816&key=<用户的key>

import requests
import json

class AmapAPI(object):
    def __init__(self, conf):
        self.params = dict()

        self.base_url = conf.getBaseUrl()
        self.params['key'] = conf.getKey()

    def geo(self, address, city='', batch=False):
        url = self.base_url + 'geocode/geo'

        self.params['city'] = city
        self.params['address'] = address
        self.params['batch'] = batch

        r = requests.get(url, params=self.params)
        r = json.loads(r.text)

        if r['status'] == '1':
            response = {
                    'status': r['status'],
                    'info': r['info'],
                    'address': r['geocodes'][0]['formatted_address'],
                    'location': r['geocodes'][0]['location'],
                    }
        else:
            response = {
                    'status': r['status'],
                    'info': r['info'],
                    'address': city + address,
                    'location': 'error',
                    }

        return response

    def riding(self, origin, destination):
        url = self.base_url + 'direction/riding'
        return self._fetch(url, origin, destination)

    # origin 'lon,lat'
    # destination'lon,lat'
    # return array from json
    def _fetch(self, url, origin, destination):
        self.params['origin'] = origin
        self.params['destination'] = destination

        r = requests.get(url, params=self.params)
        r = json.loads(r.text)
        response = dict()
        if r['status'] == '1':
            response = {
                    'status': r['status'],
                    'info': r['info'],
                    'origin': r['route']['origin'],
                    'destination': r['route']['destination'],
                    'distance': r['route']['paths'][0]['distance'],
                    'duration': r['route']['paths'][0]['duration'],
                    }
        else:
            response = {
                    'status': r['status'],
                    'info': r['info'],
                    'origin': origin,
                    'destination': destination,
                    'distance': 'error',
                    'duration': 'error',
                    }
        return response

if __name__ == "__main__":
    from conf import Conf

    api = AmapAPI(Conf('config'))
    print api.riding('116.434307,39.90909', '116.434446,39.90816')
    print api.geo(address='宗泽路60号2幢4楼', city='镇江市')
    print api.geo(address='宗泽路60号2幢4楼')
