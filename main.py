from datetime import datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from borax.calendars.festivals import LunarSchema


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
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta =today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(m,d):
  ls=LunarSchema(month=m,day=d)
  return ls.countdown()

def get_words():
  words = requests.get("http://api.guaqb.cn/v1/onesaid/")
  return words
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

ba=get_birthday(11,1)
ma=get_birthday(12,14)
me=get_birthday(12,2)
ge=get_birthday(3,18)
jie=get_birthday(5,12)
rui=get_birthday(10,4)
dujuan=get_birthday(6,5)
zw=get_birthday(10,22)
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"date":{"value":today},"weather":{"value":wea,"color":"#b0a4e3"},"city":{"value":city},"temperature":{"value":temperature,"color":"#db5a6b"},"love_days":{"value":get_count(),"color":"#44cef6"},"ba":{"value":ba,"color":"#44cef6"},"ma":{"value":ma,"color":"#44cef6"},"me":{"value":me,"color":"#44cef6"},"ge":{"value":ge,"color":"#44cef6"},"jie":{"value":jie,"color":"#44cef6"},"rui":{"value":rui,"color":"#44cef6"},"dujuan":{"value":dujuan,"color":"#44cef6"},"zw":{"value":zw,"color":"#44cef6"},"words":{"value":get_words(), "color":"#ffa631"}}
res = wm.send_template(user_id, template_id, data)
print(res)
