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

    def riding(self, origin, destination):
        url = self.base_url + '/direction/riding'
        return self._fetch(url, origin, destination)

    # origin 'lon,lat'
    # destination'lon,lat'
    # return array from json
    def _fetch(self, url, origin, destination):
        self.params['origin'] = origin
        self.params['destination'] = destination

        r = requests.get(url, params=self.params)
        r = json.loads(r.text)
        response = {
                'status': r['status'],
                'info': r['info'],
                'origin': r['route']['origin'],
                'destination': r['route']['destination'],
                'distance': r['route']['paths'][0]['distance'],
                'duration': r['route']['paths'][0]['duration'],
                }
        return response

if __name__ == "__main__":
    from conf import Conf

    api = AmapAPI(Conf('config'))
    print api.riding('116.434307,39.90909', '116.434446,39.90816')
