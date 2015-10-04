#!/usr/bin/python2.7
#coding:utf8

import requests
import json
from settings import ENV

def getAccessToken():
    form = {
        'grant_type': 'client_credentials',
        'client_secret': ENV['voice_secretkey'],
        'client_id': ENV['voice_apikey'],
    }
    body = requests.post(ENV['urls']['getAccessToken'], data=form)
    body.encoding = 'utf8'
    data = json.loads(body.text)
    return data['access_token']

def parseWeatherInfo(data):
    weather = data['HeWeather data service 3.0'][0]
    if weather['status'] != 'ok':
        return "status error"
    city = weather['basic']['city']
    now_txt = weather['now']['cond']['txt']
    now_feel = weather['now']['fl']
    now_tmp = weather['now']['tmp']
    now_hum = weather['now']['hum']
    now_wind = weather['now']['wind']['dir'] + weather['now']['wind']['sc']
    now_aqi_qity = weather['aqi']['city']['qlty']
    today_txt_d = weather['daily_forecast'][0]['cond']['txt_d']
    today_txt_n = weather['daily_forecast'][0]['cond']['txt_n']
    today_tmp_max = weather['daily_forecast'][0]['tmp']['max']
    today_tmp_min = weather['daily_forecast'][0]['tmp']['min']
    today_wind = weather['daily_forecast'][0]['wind']['dir'] +\
                    weather['daily_forecast'][0]['wind']['sc']
    tips = weather['suggestion']['sport']['txt']

    ret = city + u"今天白天，" + today_txt_d+u"，" +\
          today_tmp_min + u"到" + today_tmp_max + u"度，" +\
          today_wind + u"，" +\
          tips
    return ret

def getWeatherInfo():
    headers = {'apikey': ENV['weather_apikey']}
    body = requests.get(
        ENV['urls']['getWeather']+ENV['city'],
        headers = headers,
    )
    body.encoding = 'utf8'
    #print body.text
    data = json.loads(body.text)
    return data

def getWeatherForecast():
    data = getWeatherInfo()
    return parseWeatherInfo(data)

def postData(token, data):
    form = {
        'tex': data,
        'lan': 'zh',
        'cuid': '123456',
        'ctp': '1',
    #    'spd': '5',
        'tok': token 
    }
    body = requests.post(ENV['urls']['texToVoice'], data=form, stream=True)
    return body.content

def textToVoice(data):
    token = getAccessToken()
    voice = postData(token, data)
    if 'err_no' in voice:
        print voice
        return
    with open('temp.mp3', 'w') as f:
        f.write(voice)

if __name__ == '__main__':
    data = getWeatherForecast()
    textToVoice(data)
