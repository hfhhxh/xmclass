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

cat = '9987,653,655'
listurl = 'http://list.jd.com/list.html?cat=__cat__&page=__page__&delivery=1&stock=0&trans=1&JL=4_10_0'
producturl = 'http://item.jd.com/__skuid__.html'
priceurl = 'http://p.3.cn/prices/get?pdtk=&pduid=__uid__&pdpin=&pdbp=0&skuid=J___skuid__'
commenturls = ['http://club.jd.com/comment/getSkuProductPageComments.action?productId=__skuid__&score=0&sortType=5&page=__page__&pageSize=10&callback=fetchJSON_comment98vv__commentversion__', 'http://sclub.jd.com/comment/getSkuProductPageComments.action?productId=__skuid__&score=0&sortType=5&page=__page__&pageSize=10&callback=fetchJSON_comment98vv__commentversion__']

headers = {'User-Agent':'Mozilla/5.0'}

def getPrice(skuid) :
  req = requests.get(priceurl.replace('__uid__', str(random.randint(1, 8192))).replace('__skuid__', skuid), headers = headers) 
  html = req.text
  js = json.loads(html)
  return js[0]['p']

def getPageCount() :
	req = requests.get(listurl.replace('__cat__', cat).replace('__page__', '0'), headers = headers)
	html = req.text
	soup = BeautifulSoup(html, 'lxml')
	ret = soup.find_all('a', class_='pn-next')
	return int(ret[0].previous_element.previous_element)

def getPageSkuids(page) :
	req = requests.get(listurl.replace('__cat__', cat).replace('__page__', str(page)), headers = headers)
	html = req.text
	soup = BeautifulSoup(html, 'lxml')
	ret = soup.find_all('div', class_='gl-i-wrap j-sku-item')
	skuids = list()
	skuidPat = re.compile('(?<=item\\.jd\\.com/)\\d*(?=\\.html)')
	for div in ret :
		text = div.a['href']
		skuids.append(re.findall(skuidPat, text)[0])
	return skuids

def getProductPage(skuid) :
	req = requests.get(producturl.replace('__skuid__', skuid), headers = headers)
	html = req.text
	return html

def getSkuids(html) :
	skuidPat = re.compile('(?<="SkuId":)\d*')
	rs = re.findall(skuidPat, html)
	return rs

def getSkuname(html) :
#	skunamePat = re.compile('(?<=<div class="sku-name">).*?(?=</div>)')
#	rs = re.findall(skunamePat, html)	
	soup = BeautifulSoup(html, 'lxml')
	ret = soup.find_all('div', class_='sku-name')
	if(len(ret) == 1) :
		return ret[0].text
	ret = soup.find_all('h1')
	return ret[0].text

def getProductInfo(html) :
	soup = BeautifulSoup(html, 'lxml')
	ret = soup.find_all('div', class_='Ptable-item')
	dic = dict()
	for div in ret :
		dt = div.find_all('dt')
		dd = div.find_all('dd')
		ln = len(dt)
		for i in range(0, ln) :
			dic[dt[i].text] = dd[i].text
	return dic

def filter(skuname) :
	return skuname.find('【') != -1

def getCommentVersion(html) :
	commentVersionPat = re.compile("(?<=commentVersion:')\d*(?=')")
	rs = re.findall(commentVersionPat, html)
	return rs[0]


def getPageComment(commentcl, skuid, page, commentVersion, start, end) :
##1 succeed continue sleep 30
##0 failed  plus 1   sleep 60
##
## -1 failed sleep 60
## 0 over sleep 30
## 1 continue sleep 30
	for url in commenturls :
		ret = 0
		url = url.replace('__skuid__', skuid).replace('__page__', str(page)).replace('__commentversion__', commentVersion)
		print(url)
		req = requests.get(url, headers = headers)
		text = req.text
		if text == None or text == '' :
			continue
		ret = 1
		text = text[start:end]
#		print(text)
		try :
			js = json.loads(text)
		except :
			print(text)
			return 0
		if js.get('comments') == None :
			print(text)
			return 0
		for comment in js['comments'] :
			spec = dict()
			spec['id'] = comment['id']
			ret = commentcl.update(spec, comment, True)
			if ret['updatedExisting'] == True :
				ret = 0
		if len(js['comments']) < 10 :
			ret = 0
		return ret
	return 0 

