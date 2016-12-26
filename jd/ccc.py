#!/usr/bin/python3
import requests
import re
import sys
import time
import json
import time
import threading
import random
from lxml import etree

from pymongo import MongoClient
mongoClient = MongoClient(host='172.20.151.0', port=8001)
db = mongoClient['jd']
iphone = db['iphone']

headers = {'User-Agent':'Mozilla/5.0'}

skuid = '1856584'
itemurl = 'http://item.jd.com/'+skuid+'.html'

url0 = 'http://club.jd.com/comment/getSkuProductPageComments.action?productId='+skuid+'&score=0&sortType=5&page=__page__&pageSize=10&callback=fetchJSON_comment98vv'
url1 = 'http://sclub.jd.com/comment/getSkuProductPageComments.action?productId='+skuid+'&score=0&sortType=5&page=__page__&pageSize=10&callback=fetchJSON_comment98vv'

cmversionpat = re.compile("(?<=commentVersion:')\d*(?=')")

req = requests.get(itemurl, headers = headers)
rs = re.findall(cmversionpat, req.text)
cmversion = rs[0]

start = len('fetchJSON_comment98vv' + cmversion) + 1
end = -2

requestserror = 0
loadserror = 0
commentserror = 0
succeed = 0

print(url0.replace('__page__', '0') + cmversion)
req = requests.get(url0.replace('__page__', '0') + cmversion, headers = headers)
js = json.loads(req.text[start:end])
pages = int(js['productCommentSummary']['commentCount'])
print(pages, pages//10)
pages = pages // 10 + 1
time.sleep(100)

for page in range(0, pages) :
    print(page)
    req = requests.get(url0.replace('__page__', str(page))+cmversion, headers = headers)
    if req.text == ''  or req.text == None :
        time.sleep(60 + random.randint(0, 10))
        req = requests.get(url1.replace('__page__', str(page))+cmversion, headers = headers)
    if req.text == '' or req.text == None :
        time.sleep(60 + random.randint(0, 10))
        requestserror += 1
        continue
    try :
        js = json.loads(req.text[start:end])
    except :
        print('loads errors.', req.text[start:end])
        time.sleep(60 + random.randint(0, 10))
        loadserror += 1
        continue
    if js['comments'] == None :
        print('comments errors.', req.text[start:end])
        time.sleep(60 + random.randint(0, 10))
        commentserror += 1
        continue
    for comment in js['comments'] :
        iphone.insert(comment)
        succeed += 1
    time.sleep(60 + random.randint(0, 10))
print(requestserror, loadserror, commentserror, succeed)
