#!/usr/bin/env python
# encoding: utf-8

import sys
import csv

if __name__ == "__main__":
    argv = sys.argv
    if (len(argv) <> 4) or (argv[1] not in ['location', 'address']):
        print "*****************************************************"
        print "Usage:"
        print "    ./amap-python-client.py MODE INPUTFILE OUTPUTFILE"
        print ""
        print "    MODE:"
        print "        location: 使用经纬度查询"
        print "        address: 使用地址查询"
        print ""
        print "    EXAMPLE:"
        print "    ./amap-python-client.py location INPUTFILE OUTPUTFILE 读取poi_city和poi_address数据"
        print "    ./amap-python-client.py address INPUTFILE OUTPUTFILE 读取latitude和longitude数据"
        print "*****************************************************"
    else:
        mode = argv[1]
        input_file = argv[2]
        output_file = argv[3]

        from conf import Conf
        from amapapi import AmapAPI

        api = AmapAPI(Conf('config'))
        #print api.riding('116.434307,39.90909', '116.434446,39.90816')

        data = list()
        with open(input_file, 'rb') as inputFp:
            dialect = csv.Sniffer().sniff(inputFp.read(1024))
            inputFp.seek(0)
            reader = csv.DictReader(inputFp, dialect=dialect)
            data = [line for line in reader]

        ans = list()
        for originline in data:
            if mode == 'location':
                origin = '%.6f,%.6f' % (float(originline['longitude']), float(originline['latitude']))
            elif mode == 'address':
                originLocation = api.geo(originline['poi_address'], originline['poi_city'])
                origin = originLocation['location']
            for destline in data:
                if mode == 'location':
                    destination = '%.6f,%.6f' % (float(destline['longitude']), float(destline['latitude']))
                elif mode == 'address':
                    destinationLocation = api.geo(destline['poi_address'], destline['poi_city'])
                    destination = destinationLocation['location']

                if origin == 'error':
                    ans.append({
                        'status': originLocation['status'],
                        'info': originLocation['info'],
                        'origin': originLocation['address'],
                        'destination': 'error',
                        'distance': 'error',
                        'duration': 'error',
                        })
                elif destination == 'error':
                    ans.append({
                        'status': destinationLocation['status'],
                        'info': destinationLocation['info'],
                        'origin': 'error',
                        'destination': destinationLocation['address'],
                        'distance': 'error',
                        'duration': 'error',
                        })
                elif origin <> destination:
                    ans.append(api.riding(origin, destination))

        with open(output_file, 'wb') as outputFp:
            fieldnames = ['status', 'info', 'origin', 'destination', 'distance', 'duration']
            writer = csv.DictWriter(outputFp, fieldnames=fieldnames)
            writer.writeheader()
            for line in ans:
                writer.writerow(line)
