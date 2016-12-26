#!/usr/bin/python3
import requests
import re
import lxml
import time
import csv
from bs4 import BeautifulSoup

def getHtml(url) :
	print(url)
	time.sleep(1)
	headers={'User-Agent':'Mozilla/5.0'}
	try :
		req = requests.get(url, headers = headers)
		req.encoding = 'utf8'
		return req.text
	except :
		print(url)
		return None

def getPageCount(html) :
	soup = BeautifulSoup(html, 'lxml')
	div = soup.find('div', class_='page-box house-lst-page-box')
	if div == None :
		return 0
	text = div['page-data']
	pat = re.compile('\d+')
	ret = re.findall(pat, text)
	print(text, ret)
	if ret != None :
		return int(ret[0])
	else :
		return 0

def extract(html, city, writer) :
	soup = BeautifulSoup(html, 'lxml')
	lis = soup.findAll('li')
	for li in lis :
		l = [city]
		if not li.has_attr('data-id') :
			continue
		h2 = li.find('h2')
		if h2 != None :
			l.append(h2.a.string)
			l.append(h2.a['href'])
		else :
			l.append(None)
			l.append(None)
		span = li.find('span', class_ = 'region')
		if span != None :
			l.append(span.string)
		else :
			l.append(None)
		div = li.find('div', class_ = 'area')
		if div != None :
			text = div.text.split('-')
			if text != None and len(text) == 2 :
				l.append(text[0].strip())
				l.append(text[1].strip())
			else :
				l.append(None)
				l.append(None)
		else :
			l.append(None)
			l.append(None)
		span = li.find('span', class_ = 'onsold')	
		if div != None :
			l.append(span.string)
		else :
			l.append(None)
		span = li.find('span', class_ = 'live')	
		if div != None :
			l.append(span.string)
		else :
			l.append(None)
		average = None
		total = None	
		div = li.find('div', class_ = 'average')	
		if div != None :
			if div.text.find('元/平') != -1 :
				average = div.span.string
			elif div.text.find('万/套') != -1 :
				total = div.span.string
		div = li.find('div', class_ = 'sum_num')	
		if div != None :
			total = div.span.string
		l.append(average)
		l.append(total)
		print(l)
		writer.writerow(l)

if __name__ == '__main__' :
	html = '<div class="fc-main clear"><div class="fl citys-l"><ul><li class="clear"><span class="code-title fl">B</span><div class="city-enum fl"><a href="http://bj.fang.lianjia.com" title="北京房产网">北京</a></div></li><li class="clear"><span class="code-title fl">C</span><div class="city-enum fl"><a href="http://cd.fang.lianjia.com" title="成都房产网">成都</a><a href="http://cq.fang.lianjia.com" title="重庆房产网">重庆</a><a href="http://cs.fang.lianjia.com" title="长沙房产网">长沙</a></div></li><li class="clear"><span class="code-title fl">D</span><div class="city-enum fl"><a href="http://dl.fang.lianjia.com" title="大连房产网">大连</a></div></li><li class="clear"><span class="code-title fl">G</span><div class="city-enum fl"><a href="http://gz.fang.lianjia.com" title="广州房产网">广州</a></div></li><li class="clear"><span class="code-title fl">H</span><div class="city-enum fl"><a href="http://hz.fang.lianjia.com" title="杭州房产网">杭州</a><a href="http://you.lianjia.com/hk" title="海口房产网">海口</a></div></li><li class="clear"><span class="code-title fl">J</span><div class="city-enum fl"><a href="http://jn.fang.lianjia.com" title="济南房产网">济南</a></div></li><li class="clear"><span class="code-title fl">L</span><div class="city-enum fl"><a href="http://you.lianjia.com/ls" title="陵水房产网">陵水</a></div></li></ul></div><div class="fl citys-r"><ul><li class="clear"><span class="code-title fl">N</span><div class="city-enum fl"><a href="http://nj.fang.lianjia.com" title="南京房产网">南京</a></div></li><li class="clear"><span class="code-title fl">Q</span><div class="city-enum fl"><a href="http://qd.fang.lianjia.com" title="青岛房产网">青岛</a><a href="http://you.lianjia.com/qh" title="琼海房产网">琼海</a></div></li><li class="clear"><span class="code-title fl">S</span><div class="city-enum fl"><a href="http://sh.fang.lianjia.com" title="上海房产网">上海</a><a href="http://sz.fang.lianjia.com" title="深圳房产网">深圳</a><a href="http://su.fang.lianjia.com" title="苏州房产网">苏州</a><a href="http://sjz.fang.lianjia.com" title="石家庄房产网">石家庄</a><a href="http://you.lianjia.com/san" title="三亚房产网">三亚</a></div></li><li class="clear"><span class="code-title fl">T</span><div class="city-enum fl"><a href="http://tj.fang.lianjia.com" title="天津房产网">天津</a></div></li><li class="clear"><span class="code-title fl">W</span><div class="city-enum fl"><a href="http://wh.fang.lianjia.com" title="武汉房产网">武汉</a><a href="http://you.lianjia.com/wc" title="文昌房产网">文昌</a><a href="http://you.lianjia.com/wn" title="万宁房产网">万宁</a></div></li><li class="clear"><span class="code-title fl">X</span><div class="city-enum fl"><a href="http://xa.fang.lianjia.com" title="西安房产网">西安</a></div></li><li class="clear"><span class="code-title fl">Y</span><div class="city-enum fl"><a href="http://yt.fang.lianjia.com" title="烟台房产网">烟台</a></div></li></ul></div></div>'
	soup = BeautifulSoup(html, 'lxml')
	citys = soup.findAll('a')
	cityurl = dict()
	for city in citys :
		cityurl[city.string] = city['href']
	print(cityurl)
	file = open('loupan.csv', 'w')
	writer = csv.writer(file)
	for (city, url) in cityurl.items() :
		html = getHtml(url + '/loupan/pg')
		pageCount = getPageCount(html)
		extract(html, city, writer)
		for page in range(2, pageCount+1) :
			html = getHtml(url + '/loupan/pg' + str(page))
			extract(html, city, writer)
	file.close()
