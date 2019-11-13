import requests
import urllib
import json
import multiprocessing as mp
import pandas as pd


def get_token(image,tag):
    url = "https://auth.docker.io/token?scope=repository:"+str(image)+":pull&service=registry.docker.io"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    webContent = response.read().decode('utf-8')
    return webContent

def get_manifest(image,tag,token):
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
           'Authorization': 'Bearer '+str(token)}
    url = 'https://registry-1.docker.io/v2/'+str(image)+'/manifests/'+str(tag)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    webContent = response.read().decode('utf-8')
    return webContent

def inspect(liste):
	try:
		image = liste[0]
		tag = liste[1]
		data = json.loads(get_token(image,tag))
		token = data['token']
		manifest = json.loads(get_manifest(image,tag,token))

		if manifest['layers']:
			with open('./layers_community/'+image.replace('/',':')+':'+tag, 'w') as json_file:  
				json.dump(manifest['layers'], json_file )
	except:
		pass
	    

if __name__ == '__main__':
	images=pd.read_csv('../data/images_tags/community_tags.csv', sep=',', dtype=object, 
		#nrows=5000, 
		index_col=None, error_bad_lines=False)
	images = images[['slug','tag']]
	images.sort_values('slug', inplace = True)
	images.drop_duplicates(inplace = True)

	# create tasks
	images=images.values.tolist()

	print(len(images))

	 # MUlti processing
	pool= mp.Pool(processes=24)
	results=pool.imap_unordered(inspect,images, 100)

	pool.close()
	pool.join()
