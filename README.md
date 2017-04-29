# amap-python-client

## 系统需求
1. Python 2.7
1. Pip
1. Virtualenv(可选)

## 安装
1. pip install -r requirements.txt
1. cp config.sample config
1. 编辑config文件,将申请的key填入文件中的key字段

## 使用

### 数据文件
* 数据文件应为csv格式并以.csv作为扩展名
* 准备数据文件,数据文件应包含以下数据:
    * poi_id 地址id
    * poi_city 地址所在城市
    * poi_address 详细地址(可不包含城市)
    * latitude 纬度
    * longitude 经度

### 运行结果
* 运行结果为csv格式,并以.csv为扩展名
* 结果文件说明:
    * status 结果状态,为1代表正常,为0则运行出错
    * info 在status为0时提供高德给出的具体错误信息,在status为1时为OK
    * origin 出发点信息,正常查询时为出发点的经纬度信息,地址查询出错时为出错地址
    * destination 目的地信息,正常查询时为出发点的经纬度信息,地址查询出错时为出错地址
    * distance 骑行距离,正常查询时以米为单位,出错时为error
    * duration 骑行时间,正常查询时以秒为单位,出错时为error

### 运行
* 经纬度查询: python ./amap-python-client.py location INPUTFILE OUTPUTFILE
    * python ./amap-python-client.py location testinput.csv testoutput.csv
* 地址查询: python ./amap-python-client.py address INPUTFILE OUTPUTFILE
    * python ./amap-python-client.py address testinput.csv testoutput.csv

## 技术支持
Email: richard.ma.19850509@gmail.com
