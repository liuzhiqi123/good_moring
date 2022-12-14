from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather']+'     '+weather['wind'], math.floor(weather['temp']),math.floor(weather['high']),math.floor(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_constellation():
  fortune = requests.get("http://web.juhe.cn/constellation/getAll?consName=%E7%99%BD%E7%BE%8A%E5%BA%A7&type=today&key=75cea6e79d1d65cddbd71c688f950fb3")
  return fortune.json()['summary']

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,high,low = get_weather()



temMo = str(temperature)+'℃    今日最高:' + str(high)+'℃    最低:'+ str(low)+'℃'
data = {"weather":{"value":wea},"temperature":{"value":temMo},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"horoscope":{"value":get_constellation(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
