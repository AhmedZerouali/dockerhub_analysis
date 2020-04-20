import os
import subprocess
import multiprocessing as mp


# This is a script that pulls and runs an image and then get the output of the commands "dpkg -l" and "cat /etc/debian_version" from it.

commands = [
"docker stop $(docker ps -a -q)", 
"docker rm $(docker ps -a -q)",
"docker volume rm $(docker volume ls -qf dangling=true)",
"docker rmi -f $(docker images  | grep -v ^'debian ' | awk '{print $3}')"
]

def clean_docker():
	for cmd in commands:
		try:
			subprocess.check_call(cmd, stdout=subprocess.DEVNULL, shell=True)
		except:
			continue
		print('Finished process')

def download(image_file):
    """Pulls and runs the Docker images-f
    """
    image = image_file.split(':')

    image = str(image[0])+'/'+str(image[1])+':'+str(image[2]) # community
    #image = str(str(image[1])+':'+str(image[2])) # official
    
    os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'cat /etc/debian_version' > ../data/community/releases/"+ image_file)
    os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'dpkg -l' > ../data/community/packages/"+ image_file)


def main():
	images = [x.strip() for x in open("../data/images_tags/community_debian_images.csv").readlines()]

	l = (len(images)/300) + 1
	for i in range(0,int(l)): 
		print('Moving to the iteration number '+str(i))
		try:
			pool= mp.Pool(processes=14)
			results=pool.imap_unordered(download,images[i*300:(i+1)*300], 10)
			pool.close()
			pool.join()
			clean_docker()

		except:
			break

if __name__ == "__main__":
	# if the folders in wich the results are going to be stored do not exist, please create them, or uncomment the following line
    #os.system('mkdir ../data/community/releases/') 	# Do the same thing for official images

	clean_docker()
	main()
