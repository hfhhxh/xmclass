#!/usr/bin/python3
import requests
import re
import lxml
import time
import csv
import jieba
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
	words = dict()
	file = open('danche.csv', 'r')
	reader = csv.reader(file)
	for row in reader :
		text = row[0]
		seg_list = jieba.cut(text)
		for word in seg_list :
			if words.get(word) != None :
				words[word] = words[word] + 1
			else :
				words[word] = 1
	file.close()
	wordss = sorted(words.items(), key=lambda d:d[1], reverse = True)
	print(wordss)
