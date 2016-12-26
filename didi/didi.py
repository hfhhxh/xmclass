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

if __name__ == '__main__' :
	file = open('didi.csv', 'w')
	writer = csv.writer(file)
	url = 'http://news.baidu.com/ns?word=%E6%BB%B4%E6%BB%B4&pn=_pn_&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'
	for pn in range(0, 38) :
		html = getHtml(url.replace('_pn_', str(pn*20)))
		soup = BeautifulSoup(html, 'lxml')
		divs = soup.findAll('div', class_='result')
		for div in divs :
			l = list()
			l.append(div.h3.a.text)
			l.append(div.h3.a['href'])
			p = div.find('p', class_='c-author').text
			pps = p.split()
			for pp in pps :
				l.append(pp)
			print(l)
			writer.writerow(l)
	file.close()
