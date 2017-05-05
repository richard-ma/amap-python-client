#!/usr/bin/env python
# encoding: utf-8

import sys
import csv

if __name__ == "__main__":
    argv = sys.argv
    # 命令行参数不足，输出使用帮助
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
        print "    ./amap-pyth850509on-client.py address INPUTFILE OUTPUTFILE 读取latitude和longitude数据"
        print "*****************************************************"
    else:
        # 正式运行
        mode = argv[1] # 运行模式
        input_file = argv[2] # 输入文件名
        output_file = argv[3] # 输出文件名

        from conf import Conf
        from amapapi import AmapAPI

        api = AmapAPI(Conf('config')) # 读取配置文件，主要是api的地址和用户的高德key
        #print api.riding('116.434307,39.90909', '116.434446,39.90816')

        # 打开输入文件读入数据到data
        data = list()
        with open(input_file, 'rb') as inputFp:
            dialect = csv.Sniffer().sniff(inputFp.read(1024))
            inputFp.seek(0)
            reader = csv.DictReader(inputFp, dialect=dialect)
            data = [line for line in reader]

        ans = list()
        for originline in data: # 起点信息
            if mode == 'location':
                origin = '%.6f,%.6f' % (float(originline['longitude']), float(originline['latitude'])) # 直接使用输入文件的经纬度
            elif mode == 'address':
                originLocation = api.geo(originline['poi_address'], originline['poi_city']) # 用高德api将地址转换为经纬度
                origin = originLocation['location']
            for destline in data: # 终点信息
                if mode == 'location':
                    destination = '%.6f,%.6f' % (float(destline['longitude']), float(destline['latitude'])) # 直接使用输入文件的经纬度
                elif mode == 'address':
                    destinationLocation = api.geo(destline['poi_address'], destline['poi_city']) # 用高德api将地址转换为经纬度
                    destination = destinationLocation['location']

                if origin == 'error': # 处理起点转换地址时出错的问题
                    ans.append({
                        'status': originLocation['status'],
                        'info': originLocation['info'],
                        'origin': originLocation['address'],
                        'destination': 'error',
                        'distance': 'error',
                        'duration': 'error',
                        })
                elif destination == 'error': # 处理终点转换地址时出错的问题
                    ans.append({
                        'status': destinationLocation['status'],
                        'info': destinationLocation['info'],
                        'origin': 'error',
                        'destination': destinationLocation['address'],
                        'distance': 'error',
                        'duration': 'error',
                        })
                elif origin <> destination: # 起点和终点地址都正确转换为经纬度或直接就是经纬度形式，则进行路径规划查询
                    ans.append(api.riding(origin, destination)) # 从高德读取数据并保存到ans中

        # 输出到输出文件
        with open(output_file, 'wb') as outputFp:
            fieldnames = ['status', 'info', 'origin', 'destination', 'distance', 'duration']
            writer = csv.DictWriter(outputFp, fieldnames=fieldnames)
            writer.writeheader()
            for line in ans:
                writer.writerow(line)
