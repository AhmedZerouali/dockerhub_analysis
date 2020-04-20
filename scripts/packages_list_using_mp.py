import json as js
import os
import codecs
import subprocess
import pandas as pd
import multiprocessing as mp

# get packages and their versions found installed in countainers; from "dpkg -l" and release files

def parse_packages(lista):
    columns=['name','package','version']
    data = pd.DataFrame(columns=columns)
    for index, dir, file in lista:
        command_package="grep ^ii "+dir+file 

        proc = subprocess.Popen(command_package, stdout=subprocess.PIPE, shell=True)
        lines = list(filter(lambda x:len(x)>0,(line.strip().decode('utf-8') for line in proc.stdout)))
        packages=[]
        versions=[]
        for line in lines:
            line=line.split(' ')
            line=sorted(set(line), key=lambda x: line.index(x))
            packages.append(line[2])
            versions.append(line[3])

        df = pd.DataFrame({'name' : file, 'package' : packages,'version' : versions})
        data=data.append(df)
    return data

def parse_releases(lista):
    releases=[]
    files=[]
    for index, dir, file in lista:
        with open(dir+file) as lines:
            for line in lines.readlines():
                release=line.strip('\n')

        files.append(file)
        releases.append(release)
    data = pd.DataFrame({'name' : files, 'release' : releases})  
    return data

def listdir_fullpath(dir):
    return [[i,dir,f] for i, f in enumerate(os.listdir(dir))]

def main():
    dirs = ['../data/official/','../data/community/']
    types = ['official','community']

    for i, dir in enumerate(dirs):
        dir=dir + 'packages/'
        list_dirs = listdir_fullpath(dir)
        chunks = [list_dirs[x:x+100] for x in range(0, len(list_dirs), 100)]
        pool= mp.Pool(processes=24)
        results=pool.imap_unordered(parse_packages, chunks, 100)

        # Get the results
        columns=['name','package','version']
        packages = pd.DataFrame(columns=columns)
        for res in results:
            packages = packages.append(res)
        packages.to_csv('../csv/list_pkgs_rels/'+types[i]+'_packages.csv', index=False)

    for i, dir in enumerate(dirs):
        dir=dir + 'releases/'
        list_dirs = listdir_fullpath(dir)
        chunks = [list_dirs[x:x+1000] for x in range(0, len(list_dirs), 1000)]
        pool= mp.Pool(processes=24)
        results=pool.imap_unordered(parse_releases, chunks, 1000)

        # Get the results
        columns=['name','release']
        releases = pd.DataFrame(columns=columns)
        for res in results:
            releases = releases.append(res)
        releases.to_csv('../csv/list_pkgs_rels/'+types[i]+'/_releases.csv', index=False)


if __name__ == "__main__":
    main()