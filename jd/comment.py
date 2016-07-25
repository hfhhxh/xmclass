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

while True :
	skuid = redisClient.blpop('cpending', 60)
	errors = 0
	if skuid == None :	##
		break
	skuid = skuid[1]
	print(skuid)
	redisClient.sadd('cvisited', skuid)
	redisClient.srem('cinpending', skuid)
	html = getProductPage(skuid)
	commentVersion = getCommentVersion(html)
	start = len('fetchJSON_comment98vv') + len(commentVersion) + 1
	end = -2
	page = -1	
	while True :
		page += 1
		ret = getPageComment(commentcl, skuid, page, commentVersion, start, end)
		if ret == 0 :
			time.sleep(60 + random.randint(-10, 10))
			errors += 1
			if errors == 100 :
				break
		elif ret == 1 :
			time.sleep(30 + random.randint(-10,10))
