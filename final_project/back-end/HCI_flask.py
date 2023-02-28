import re
from random import randint
from flask import Flask, request
from KDXF import *
import requests
import time

app = Flask(__name__)


# **市的天气/**的天气/**天气/**市天气
def getWeather(f_str):
    location = f_str.split('天气')[0]
    if location.find("的"):
        location = location.split('的')[0]
    if location.find("市"):
        location = location.split('市')[0]
    url = 'https://www.tianqiapi.com/free/day?appid=56761788&appsecret=ti3hP8y9&city={}'.format(location)
    res = requests.get(url=url)
    res = json.loads(res.content)
    return "{}今天的天气情况为{},温度为{}摄氏度".format(res["city"], res["wea"], res["tem"]), True


# 新闻（随机返回一条新闻）
def getNews():
    url = 'https://way.jd.com/jisuapi/get?channel=头条&num=10&start=0&appkey=da39dce4f8aa52155677ed8cd23a6470'
    res = requests.get(url=url)
    res = json.loads(res.content)
    news_len = len(res["result"]["result"]["list"])
    res_data = res["result"]["result"]["list"][randint(0, news_len)]["title"]
    return res_data, True


# # 翻译"****"(仅支持中英互翻)
# def getTranslate(f_str):
#     cont = f_str.split('翻译')[1]
#     remove_chars ='[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'
#     cont = re.sub(remove_chars,"", cont)
#     url = 'https://api.66mz8.com/api/translation.php?info={}'.format(cont)
#     res = requests.get(url=url)
#     res = json.loads(res.content)
#     return res["fanyi"], True


# “上海”尾号限行政策
def getLimit(f_str):
    location = f_str.split('尾号限行')[0]
    if location.find("的"):
        location = location.split('的')[0]
    if location.find("市"):
        location = location.split('市')[0]
    city_code = ''
    city_name_url = 'https://open.liupai.net/vehiclelimit/city?appkey=5641cb5f59a4890b05c015fe3629ea31'
    city_res = requests.get(url=city_name_url, verify=False)
    city_res = json.loads(city_res.content)
    for item in city_res["result"]:
        if item["cityname"] == location:
            city_code = item["city"]
    if city_code == '':
        return '没有该城市的限行政策', False
    url = 'https://open.liupai.net/vehiclelimit/query?appkey=5641cb5f59a4890b05c015fe3629ea31&city={}&date'.format(city_code)
    res = requests.get(url=url, verify=False)
    res = json.loads(res.content)
    return "地点：{} {}".format(res["result"]["area"], res["result"]["summary"]), True


# **市**路的路况（只可以地级市）
def getRoadSituation(f_str):
    location = f_str.split('路况')[0]
    if location.find('市') >= 0:
        city = location.split('市')[0]
        road_name = location.split('市')[1].split('的')[0]
    else:
        return '请输入正确的地点', False
    url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak=7khcth5v6N9ddhW0spLMGg8ZuF5HAbzq'.format(road_name, city)
    res = requests.get(url=url)
    res = json.loads(res.content)
    if res['message'] != '成功':
        return '请输入正确的地点', False
    return res['description'], True


# **市的灾害
def getWarning(f_str):
    location = f_str.split('的')[0]
    city_url = 'https://geoapi.qweather.com/v2/city/lookup?location={}&key=de2d83e9e969454587f1547915c066f8'.format(location)
    city_res = requests.get(url=city_url)
    city_res = json.loads(city_res.content)
    city_id = city_res['location'][0]['id']
    url = 'https://devapi.qweather.com/v7/warning/now?location={}&key=de2d83e9e969454587f1547915c066f8'.format(city_id)
    res = requests.get(url=url)
    res = json.loads(res.content)
    if not res['warning']:
        return '该地区没有气象灾害', True
    return res['warning'][0]['text'], True


@app.route('/speechProcess', methods=['GET','POST'])
def processSpeech():
    mp3_file = request.files['file']
    mp3_file.save("myRecode.mp3")
    mp3_to_pcm(mp3_file.filename)
    client = Client()
    client.send('./send.pcm')
    time.sleep(1)
    f = open("result.txt", "r")
    f_str = f.readline()
    print("读取的字符串是:{}".format(f_str))
    if '天气' in f_str:
        result, status = getWeather(f_str)
        type = 3
    elif '新闻' in f_str:
        result, status = getNews()
        type = 3
    # elif '翻译' in f_str:
    #     result, status = getTranslate(f_str)
    #     type = 3
    elif '尾号限行' in f_str:
        result, status = getLimit(f_str)
        type = 3
    elif '路况' in f_str:
        result, status = getRoadSituation(f_str)
        type = 3
    elif '灾害' in f_str:
        result, status = getWarning(f_str)
        type = 3
    elif '电话' in f_str:
        result = re.findall(r'\d+', f_str)[0]
        if result == '':
            status = False
        else:
            status = True
        type = 1
    elif '短信' in f_str:
        result = re.findall(r'\d+', f_str)[0]
        if result == '':
            status = False
        else:
            status = True
        type = 2

    elif '相机' in f_str:
        result = '已打开'
        type = 4
        status = True

    elif ('向前' in f_str) or ('前进' in f_str):
        result = '好的'
        type = 5 # 前进指令标志
        status = True

    elif ('向后' in f_str) or ('后退' in f_str):
        result = '好的'
        type = 6 # 后退指令标志
        status = True

    elif ('向左' in f_str) or ('左' in f_str):
        result = '好的'
        type = 7 # 向左指令标志
        status = True

    elif ('向右' in f_str) or ('右' in f_str):
        result = '好的'
        type = 8 # 前进指令标志
        status = True

    else:
        result = '该功能未开放，敬请期待'
        status = False
        type = 3
    return {
        "result": result,
        "status": status,
        "type": type
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
