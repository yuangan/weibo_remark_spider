#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#爬取杨紫某条微博热评

import requests
import time
import os
import csv
import codecs
import sys
import json
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

#要爬取热评的起始url
url='https://m.weibo.cn/comments/hotflow?id=4281529376833502&mid=4281529376833502&max_id='
headers={
		'Cookie':'Your Cookie',
		'Referer': 'https://m.weibo.cn/detail/4281013208904762',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest'
		}

#存为csv
path = os.getcwd()+"/weibo.csv"
csvfile = open(path, 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
#First Row
writer.writerow(('Usename', 'Time', 'Like_count','Floor_number','Sourse', 'Comments'))

def get_page(max_id, id_type):
#参数
	params={
			'max_id':max_id,
			'max_id_type': id_type
			}
	try:
		r=requests.get(url, params=params, headers=headers)
		if r.status_code==200:
			return r.json()
	except requests.ConnectionError as e:
		print('error',e.args)

def parse_page(jsondata):
	if jsondata:
		items=jsondata.get('data')
		item_max_id={}
		item_max_id['max_id']=items['max_id']
		item_max_id['max_id_type']=items['max_id_type']
		return item_max_id

def write_csv(jsondata):
		datas = jsondata.get('data').get('data')
		for data in datas:
			created_at = data.get("created_at")
			like_count = data.get("like_count")
			source = data.get("source")
			floor_number = data.get("floor_number")
			username = data.get("user").get("screen_name")
			comment = data.get("text")
			comment = BeautifulSoup(comment,'lxml').get_text()
			#print jsondata.dumps(comment, encoding="UTF-8", ensure_ascii=False)
			writer.writerow((username, created_at, like_count, floor_number, source,json.dumps(comment, encoding="UTF-8", ensure_ascii=False)))
		
maxpage = 1000
m_id = 0
id_type = 0
for page in range(0,maxpage):
	print(page)
	jsondata=get_page(m_id, id_type)
	write_csv(jsondata)
	results=parse_page(jsondata)
	time.sleep(1)
	m_id=results['max_id']
	id_type=results['max_id_type']






























