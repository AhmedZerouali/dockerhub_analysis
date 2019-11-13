import json as js
import os
import codecs
import subprocess
import pandas as pd

# This is a parser: it parses a file that has the output of the command "dpkg -l".
# This parser returns the name of installed packages and their versions


def parse_packages():
    columns=['name','package','version']
    data = pd.DataFrame(columns=columns)
    dir='../other_containers/packages/'
    for index, file in enumerate(sorted(os.listdir(dir))):
        #if index ==100:
        #   break
        print(index,file)
        command_package="grep ^ii "+dir+file # sed 's/  */ /g' | 

        proc = subprocess.Popen(command_package, stdout=subprocess.PIPE, shell=True)
        lines = list(filter(lambda x:len(x)>0,(line.strip().decode('utf-8') for line in proc.stdout)))
        packages=[]
        versions=[]
        for line in lines:
            line=line.split(' ')
            line=sorted(set(line), key=lambda x: line.index(x))
            packages.append(line[2])
            versions.append(line[3])

        df = pd.DataFrame({'name':file, 'package':packages,'version':versions})
        data=data.append(df)
    return data.set_index('name')

def parse_releases():
    releases=[]
    files=[]
    dir='../other_containers/releases/'
    for index, file in enumerate(sorted(os.listdir(dir))):
        #if index ==100:
        #   break
        with open(dir+file) as lines:
            for line in lines.readlines():
                release=line.strip('\n')

        files.append(file)
        releases.append(release)
    data = pd.DataFrame({'name':files, 'release':releases})  
    return data.set_index('name')


def main():
    packages=parse_packages()
    releases=parse_releases()
    print(len(packages),len(releases))
    data=packages.merge(
              releases,
              left_index=True, 
              right_index=True, how='outer')
    print('taille:',len(data))

    data.to_csv('../packages_extracted.csv', sep=';', index=True)

if __name__ == "__main__":
    main()
