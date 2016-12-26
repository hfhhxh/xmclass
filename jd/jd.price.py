#!/bin/python3
import requests
import re
import time
import json
from lxml import etree
from Queue import Queue
from Stack import Stack

url = 'http://p.3.cn/prices/get?skuid=J_'

file = open('jd.out/jd.out.out', 'r')
out = open('jd.out/jd.out.price', 'w')

for line in file :
    req = requests.get(url+line[0:line.find('\t')])
    js = json.loads(req.text)
    print('{}\t\t{}'.format(line[0: len(line)-1], js[0]["p"]))
    out.write('{}\t\t{}\n'.format(line[0: len(line)-1], js[0]["p"]))
    

file.close()
out.close()
