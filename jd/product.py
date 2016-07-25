#!/usr/bin/python3
import requests
import json
import re
import time
import random
from lxml import etree
from rediscluster import StrictRedisCluster
from pymongo import MongoClient
from bs4 import BeautifulSoup
from jd import *

from rediscluster import StrictRedisCluster
startup_nodes = [{"host": "172.20.151.0", "port": "7001"},{"host": "172.20.151.0", "port": "7002"},{"host": "172.20.151.0", "port": "7003"}]
redisClient = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

from pymongo import MongoClient
mongoClient = MongoClient(host='172.20.151.0', port=8001)
db = mongoClient['jd']
productcl = db['product']
commentcl = db['comment']

pageCount = getPageCount()
print(pageCount)
for page in range(0, pageCount) :
	skuids = getPageSkuids(page)
	for skuid in skuids :
		if redisClient.sismember('inpending', skuid) == False and redisClient.sismember('visited', skuid) == False and redisClient.sismember('filtered', skuid) == False :
			ret = redisClient.sadd('inpending', skuid)
			if ret == 1 :	##
				redisClient.rpush('pending', skuid)

while True :
	skuid = redisClient.blpop('pending', 60)
	if skuid == None :	##
		break
	skuid = skuid[1]
	print(skuid)
	html = getProductPage(skuid)
	skuname = getSkuname(html)
	redisClient.set(skuid, skuname)
	if filter(skuname) :
		redisClient.sadd('filtered', skuid)
		redisClient.srem('inpending', skuid)
		continue
	else :
		redisClient.sadd('visited', skuid)
		redisClient.srem('inpending', skuid)
		if redisClient.sismember('cinpending', skuid) == False and redisClient.sismember('cvisited', skuid) == False :
			ret = redisClient.sadd('cinpending', skuid)
			if ret == 1 : ##
				redisClient.rpush('cpending', skuid)
	price = getPrice(skuid)
	dic = getProductInfo(html)	
	dic['price'] = price
	dic['skuid'] = skuid
	dic['skuname'] = skuname
	productcl.insert(dic)
	
	ids = getSkuids(html)
	for id in ids :
		if redisClient.sismember('inpending', id) == False and redisClient.sismember('visited', id) == False and redisClient.sismember('filtered', id) == False :
			ret = redisClient.sadd('inpending', id)
			if ret == 1 :	##
				redisClient.lpush('pending', id)

