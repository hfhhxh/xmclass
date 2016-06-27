#!/bin/python3
import requests
import re
import json
import time
from lxml import etree
from Queue import Queue
from Stack import Stack

#url = 'http://list.jd.com/list.html?cat=9987,653,655&page='
url = 'http://list.jd.com/list.html?cat=9987,653,655&delivery=1&stock=0&page='
itemurl = 'http://item.jd.com/'
priceurl = 'http://p.3.cn/prices/get?skuid=J_'

cat = '9987,653,655'
pagecount = 44

dic = dict()
skuids = set()
#【

itempat = re.compile('item\.jd\.com/\d*\.html')
skuidpat1 = re.compile('(?<=item\.jd\.com/)\d*(?=\.html)')
skuidpat2 = re.compile('(?<="SkuId":)\d*')
titleh1 = re.compile('(?<=<h1>).*?(?=</h1>)')
titlediv = re.compile('(?<=<div class="sku-name">).*?(?=</div>)')

for page in range(1, pagecount+1) :
    req = requests.get(url+str(page))
    html = req.text
    uids = re.findall(skuidpat1, html)
    for uid in uids :
        skuids.add(uid)

q = Queue()
for skuid in skuids:
    q.enqueue(skuid)

cnt = 0
fail = 0
filt = 0

vis = set()
while q.isEmpty() == False :
    cnt += 1
    skuid = q.dequeue();
    vis.add(skuid)
    print(len(q.items), len(vis), skuid)
    try :
        req = requests.get(itemurl + skuid + '.html', timeout = 5)
    except :
        q.enqueue(skuid)
        fail += 1;
        print("requests error.")
        time.sleep(5)
        continue
    html = req.text
    rsth1 = re.findall(titleh1, html)
    rsth2 = re.findall(titlediv, html)
    rst = rsth1 + rsth2
    if len(rst) == 1:
        title = rst[0]
        if '【' not in title :
            req = requests.get(priceurl+skuid);
            js = json.loads(req.text)
            price = js[0]['p']
            dic[skuid] = [title, price]
            print(skuid, price, title)
            file = open("jd.out/" + skuid, 'w')
            file.write(html)
            file.close()
        else :
            filt += 1
    else :
        print(rst)
    skuids = re.findall(skuidpat2, html)
    for uid in skuids :
        if uid not in vis and uid not in q.items :
            q.enqueue(uid)

print(len(vis), len(dic), cnt, fail, filt)

file = open('jd.out/jd.outre', 'w')
for key,value in dic.items():
#    print(key, value)
    file.write('{}\t{}\t{}\n'.format(key, value[0], value[1]))
file.close()


#        if id not in skuids and id not in dic:
#            req = requests.get(itemulr + id + '.html')
#            html = req.text
#            iids = re.findall(skuidpat2)
#            rst = re.findall(titlepat)
#            title = rst[0].text


#    root = etree.HTML(html)
#    lt = root.xpath('//a[@target="_blank"]/em')
#    for l in lt :
#        print(l.text)
