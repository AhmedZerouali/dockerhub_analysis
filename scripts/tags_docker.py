import json
import urllib.request
import pandas as pd
import re

# This script returns the tagged images found in a DockerHub repository.

def download(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	req = urllib.request.Request(url, headers=hdr)
	response = urllib.request.urlopen(req)
	webContent = response.read().decode('utf-8')
	return webContent

def parse(f,url,slug):
	data = json.loads(download(url))

	for result in data['results']:
		tag=str(result['name'])
		full_size=str(result['full_size'])
		last_updated=str(result['last_updated'])
		line = ','.join([slug,tag,full_size,last_updated])
		f.write(line+'\n')

def store():
	images=pd.read_csv('../csv/official_images.csv', sep=',', dtype=object, index_col=None,  usecols=['slug','publisher'], error_bad_lines=False)
	f=open('../csv/official_tags.csv','w')
	images = images.query('publisher == "Docker"')

	for index, row in enumerate(images.iterrows()):
		print('store',index)
		slug=row[1]['slug']
		page = 1
		while(True):
			url="https://registry.hub.docker.com/v2/repositories/library/"+str(slug)+"/tags/?page="+str(page)+"&page_size=100"
			try:
				parse(f,url,slug)
			except:
				break
			page = page +1

	f.close()

def community():
	images=pd.read_csv('../csv/community_images.csv', sep=',', dtype=object, index_col=None, error_bad_lines=False)
	images['popularity'] = images['popularity'].apply(int)
	images.sort_values('popularity', ascending=False, inplace=True)
	images = images.groupby('slug').first().reset_index()
	print(len(images))
	f=open('../csv/community_tags.csv','a')

	for index, row in enumerate(images.iterrows()):
		print('community', index)
		# if index<895:
		# 	continue
		slug=row[1]['slug']
		#page = 1
		#while(True):
		url="https://registry.hub.docker.com/v2/repositories/"+str(slug)+"/tags/?page=1&page_size=100"
		try:
			parse(f,url,slug)
		except:
			pass
			#page = page +1

	f.close()

store()
#community()
