import re
import json
import requests
from tqdm import tqdm
import pandas as pd
import multiprocessing as mp


# This script inspects an image in DockerHub and gets its Dockerfile commands with other information like the layers SHA

def download_url(url):
    ''' Download an url and returns the content'''
    
    response = requests.get(url)
    webContent  = response.json()
    return webContent

def image_metadata(url, source):
    ''' Parse a json file from url  '''
    
    names = []
    pops = []
    data  = download_url(url)
    for element in data['summaries']:
        popularity=str(element['popularity'])
        if source == "official":
            name=str(element['slug'])
        else:
            name=str(element['name'])
        names.append(name)
        pops.append(popularity)
    df = pd.DataFrame({'name': names, 'popularity': pops})
    return df


def number_images(url):
    ''' Returns the number of images returned in a query '''

    data=download_url(url)
    try:
        number = int(data['count'])
    except:
        return 0
    return number

def official_images():
    ''' Extract the names of official images  '''

    df_all = pd.DataFrame()
    url_option = 'https://store.docker.com/api/content/v1/products/search/?q=+&type=image&page='
    page = 1
    while(True):
        url = url_option + str(page) + "&page_size=100"
        try:
            df = image_metadata(url, 'official')
        except:
            break
        df_all = pd.concat([df_all,df])
        page = page + 1
    return df_all

def community_helper(string):
    ''' This is a helper to the "community_images()" function '''

    df_all = pd.DataFrame()
    url_option = 'https://store.docker.com/api/content/v1/products/search?q='
    page = 1
    while(True):
        url = url_option + string +"&source=community&type=image&page="+str(page)+"&page_size=100"
        try:
            df = image_metadata(url, 'community')
        except:
            break
        df_all = pd.concat([df_all,df])
        page = page + 1
    return df_all 


def community_images():
    ''' Extract the names of all community images  '''
    
    df_all = []
    url_option = 'https://store.docker.com/api/content/v1/products/search?q='
    options = '&source=community&type=image&page=1&page_size=100'
    stringer = 'abcdefghijklmnopqrstuvwxyz0123456789'
    stringer = 'a'
    for c1 in tqdm(stringer):
        for c2 in stringer:
            url = url_option + c1 + c2 + options
            number  = number_images(url)
            if number > 10000:
                for c3 in stringer:
                    url = url_option + c1 + c2 + c3+ options
                    df_all.append(community_helper(c1+c2+c3))
            else:
                df_all.append(community_helper(c1+c2))
    df_all = pd.concat(df_all)
    df_all.drop_duplicates(inplace=True)
    df_all = df_all.groupby(['name']).first().reset_index()
    return df_all
                           

def extract_tags(url):
    ''' Returns the tags available for a certain repository '''

    data = download_url(url)
    tags = []
    size = []
    date = []
    for result in data['results']:
        tags.append(str(result['name']))
        size.append(str(result['full_size']))
        date.append(str(result['last_updated']))
    df = pd.DataFrame({'tag': tags, 'full_size': size, 'last_updated': date})
    return df

def official_tags(name):
    ''' Returns the tags available for a certain OFFICIAL repository '''

    df_all = pd.DataFrame()
    page = 1
    while(True):
        url="https://registry.hub.docker.com/v2/repositories/library/"+str(name)+"/tags/?page="+str(page)+"&page_size=100"
        try:
            df_all = pd.concat([df_all, extract_tags(url)])
        except :
            break
        page = page +1
            
    return df_all
        

def community_tags(name):
    ''' Returns the tags available for a certain COMMUNITY repository '''

    df_all = pd.DataFrame()
    page = 1
    while(True):
        url="https://registry.hub.docker.com/v2/repositories/"+str(name)+"/tags/?page="+str(page)+"&page_size=100"
        try:
            df_all = pd.concat([df_all, extract_tags(url)])
        except:
            break
        page = page +1
    return df_all

def get_token(image,tag):
    ''' Returns the token needed to inspect the layers of a Docker image'''

    url = "https://auth.docker.io/token?scope=repository:"+str(image)+":pull&service=registry.docker.io"
    token = download_url(url)
    return token['token']


def get_manifest(image,tag,token):
    ''' Returns the manifest of an image containing layer ids '''

    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
           'Authorization': 'Bearer '+str(token)}
    url = 'https://registry-1.docker.io/v2/'+str(image)+'/manifests/'+str(tag)
    
    response = requests.get(url, headers=headers)
    return response.json()

def get_fsLayer(image,tag,token):
    ''' Returns the manifest of an image containing layer ids and their commands'''

    headers = {'Authorization': 'Bearer '+str(token)}
    url = 'https://registry-1.docker.io/v2/'+str(image)+'/manifests/'+str(tag)
    
    response = requests.get(url, headers=headers)
    return response.json()


def inspect_dict(name, tag):
    ''' Parse the manifest result and return the information needed as a dict variable'''

    token = get_token(name,tag)
    manifest = get_fsLayer(name,tag,token)
    image_layers = {}
    image_layers ['name'] = name
    image_layers ['tag'] = tag
    image_layers ['layers'] = []
    for i, blob in enumerate(manifest['fsLayers']):
        command = json.loads(manifest['history'][i]['v1Compatibility'])['container_config']['Cmd'][-1]
        command = command.replace('/bin/sh -c #(nop) ','').replace('/bin/sh -c','RUN')
        if command.lstrip().startswith('set'):
            command = 'RUN '+command
        layer = {}
        layer['blob'] = blob['blobSum'].split(':')[-1]        
        layer['order'] = len(manifest['fsLayers']) - i
        layer['created'] = json.loads(manifest['history'][i]['v1Compatibility'])['created']
        layer['command'] = command
        image_layers ['layers'].append(layer)
    
    return image_layers, token


def inspect_df(name, tag):
    ''' Parse the manifest result and return the information needed as a dataframe'''

    token = get_token(name,tag)
    manifest = get_fsLayer(name,tag,token)
    blobsums = []
    commands = []
    creation = []
    for i, blob in enumerate(manifest['fsLayers']):
        blobsums.append(blob['blobSum'].split(':')[-1])
        command = json.loads(manifest['history'][i]['v1Compatibility'])['container_config']['Cmd'][-1]
        command = command.replace('/bin/sh -c #(nop) ','').replace('/bin/sh -c','RUN')
        if command.lstrip().startswith('set'):
            command = 'RUN '+command
        commands.append(command)
        creation.append(json.loads(manifest['history'][i]['v1Compatibility'])['created'])
        
    df = pd.DataFrame({'blob':reversed(blobsums), 
                       'created':reversed(creation), 
                       'command': reversed(commands)
                      })
    return df

def inspect_image(image):
    name = '/'.join(image.split(':')[0:2])
    tag = image.split(':')[-1]
    try: 
        df = inspect_df(name, tag).assign(image= image)
    except: 
        df = pd.DataFrame()
    return df

if __name__ == "__main__":

	packages = pd.read_csv('../data/for_analysis/installed_packages.csv', usecols=['image','type'])
	packages.drop_duplicates(inplace=True)
	
	# Create tasks
	images=packages.image.values.tolist()

	# MUlti processing
	pool= mp.Pool(processes=28)
	results=pool.imap_unordered(inspect_image, images, 200)

	# get results
	tab=[]
	for df in results:
	    tab.append(df)
	tab = pd.concat(tab)

	# Close
	pool.close()
	pool.join()

	tab.to_csv('../data/for_analysis/commands_all_images.csv', index=False)