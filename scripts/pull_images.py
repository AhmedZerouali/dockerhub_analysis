import os
import subprocess
import multiprocessing as mp


# This is a script that pulls and runs an image and then get the output of the command "dpkg -l" from it.

commands = [
"docker stop $(docker ps -a -q)", 
"docker rm $(docker ps -a -q)",
"docker volume rm $(docker volume ls -qf dangling=true)",
"docker rmi -f $(docker images  | grep -v ^'debian ' | awk '{print $3}')"
]

def clean_docker():
	for cmd in commands:
		print(cmd)
		try:
			subprocess.check_call(cmd, stdout=subprocess.DEVNULL, shell=True)
		except:
			continue
		#p.wait()
		print('Finished process')

def download(image_file):
    """Pulls and runs the Docker images-f
    """
    image = image_file.split(':')

    image = str(image[0])+'/'+str(image[1])+':'+str(image[2]) # community
    #image = str(str(image[1])+':'+str(image[2])) # official

    os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'cat /etc/debian_version' > /home/azerouali/docker_emse/containers_pulled/releases/"+ image_file)

    os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'dpkg -l' > /home/azerouali/docker_emse/containers_pulled/packages/"+ image_file)


def main():
	done_images = [x.strip() for x in open("/home/azerouali/docker_emse/csv/done_images").readlines()]

	images = [x.strip() for x in open("/home/azerouali/docker_emse/csv/community_debian_images.csv").readlines()]

	print(len(images))
	for element in done_images:
		images.remove(element)
	print(len(images))

	images = images[0:14]
	l = (len(images)/300) + 1
	
	for i in range(0,int(l)): #3077
		print('Moving to the iteration number '+str(i))
		try:
			pool= mp.Pool(processes=14)
			#results=pool.imap_unordered(download,images[i*300:(i+1)*300], 10)
			results=pool.imap_unordered(download,images[0:14], 1)
			pool.close()
			pool.join()

			clean_docker()

		except:
			break


if __name__ == "__main__":
	clean_docker()
	main()
