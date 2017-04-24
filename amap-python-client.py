#!/usr/bin/env python
# encoding: utf-8

import sys
import csv

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) <> 3:
        print "*****************************************************"
        print "Usage:"
        print "    ./amap-python-client.py INPUTFILE OUTPUTFILE"
        print "*****************************************************"
    else:
        input_file = argv[1]
        output_file = argv[2]

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
            origin = '%.6f,%.6f' % (float(originline['longitude']), float(originline['latitude']))
            for destline in data:
                destination = '%.6f,%.6f' % (float(destline['longitude']), float(destline['latitude']))
                if origin <> destination:
                    ans.append(api.riding(origin, destination))

        with open(output_file, 'wb') as outputFp:
            fieldnames = ['status', 'info', 'origin', 'destination', 'distance(meter)', 'duration(second)']
            writer = csv.DictWriter(outputFp, fieldnames=fieldnames)
            writer.writeheader()
            for line in ans:
                writer.writerow(line)
