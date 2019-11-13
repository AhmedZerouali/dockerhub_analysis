import re
import json
from pprint import pprint
import codecs
import urllib.request

# This script returns all image repositories found in DockerHub


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

def parse(f,url):
	data = json.loads(download(url))
	#try:
	print(len(data['summaries']))
	for element in data['summaries']:
		name=str(element['name'])
		slug=str(element['slug'])
		type2=str(element['type'])
		created_at=str(element['created_at'])
		updated_at=str(element['updated_at'])
		popularity=str(element['popularity'])
		certification_status=str(element['certification_status'])
		publisher=str(element['publisher']['name'])

		try:
			operating_systems='"'
			for t in element['operating_systems']:
						operating_systems=operating_systems+str(t['name'])+';'
			operating_systems=operating_systems+'"'
		except:
			operating_systems = 'None'

		try:
			categories='"'
			for t in element['categories']:
						categories=categories+str(t['name'])+';'
			categories=categories+'"'
		except:
			categories = 'None'

		try:
			architectures = '"'
			for t in element['architectures']:
						architectures=architectures+str(t['name'])+';'
			architectures=architectures+'"'
		except:
			architectures = 'None'

		line = ','.join([slug,type2,created_at,updated_at,popularity,publisher,certification_status,name,operating_systems,categories,architectures])
		f.write(line+'\n')


def parse2(f,url):
	data = json.loads(download(url))
	for element in data['summaries']:
		name=str(element['name'])
		popularity=str(element['popularity'])

		line = ','.join([name,popularity])
		f.write(line+'\n')


def store():
	f=open('../csv/official_images_3d_try.csv','w')
	for count in range(1,6):
		print(count)
		url="https://store.docker.com/api/content/v1/products/search/?q=+&type=image&page="+str(count)+"&page_size=100"
		parse(f,url)
	f.close()

def community():
	# In case you just want a huge number of repositories
	f=open('../csv/community_images.csv','a')
	for c1 in 'qrstvwxz0123456789':
		for c2 in 'aeiouybcdfghjklmnpqrstvwxz0123456789':
			for count in range(1,101):
				print(c1+c2,count)

				url="https://store.docker.com/api/content/v1/products/search?q="+c1+c2+"&source=community&type=image&page="+str(count)+"&page_size=100"
				try:
					parse2(f,url)
				except:
					break
	f.close()

def parse_number(url):
	data = json.loads(download(url))
	try:
		number = int(data['count'])
	except:
		return 0
	return number

def community2():
	# In case you want ALMOST ALL repositories
	f=open('../csv/community_images.csv','a')
	for c1 in 'rstvwxz0123456789':
		for numero, c2 in enumerate('aeiouybcdfghjklmnpqrstvwxz0123456789'):
			if c1 == 'r' and numero <18:
				continue
			url = "https://store.docker.com/api/content/v1/products/search?q="+c1+c2+"&source=community&type=image&page=1&page_size=100"
			number  = parse_number(url)
			if number >10000:
				for c3 in 'aeiouybcdfghjklmnpqrstvwxz0123456789':
					for count in range(1,101):
						print(c1+c2+c3,count)

						url="https://store.docker.com/api/content/v1/products/search?q="+c1+c2+c3+"&source=community&type=image&page="+str(count)+"&page_size=100"
						try:
							parse2(f,url)
						except:
							break

			else:
				continue

	f.close()


community2()
