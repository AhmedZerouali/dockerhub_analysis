### This folder contains all scripts used to fetch data from DockerHub API, pull and run images, and parse the list of package.


- *tags_docker.py*: yields all tags of images found in a DockerHub repository.
- *docker_images.py*: yields all image repositories found in DockerHub.
- *inspec_docker.py*: inspecst DockerHub API and gets the layers of DockerHub images and then save the output as a json file
- *pull_images.py*: pulls and runs an image and then get the output of the commands "dpkg -l" and "cat /etc/debian_version" from it.
- *packages_list_using_mp.py*: parses packages and their versions found installed in countainers; from "dpkg -l" and release files.
- *get_bugs.py*: # extracts package bugs from UDD, it is taken from https://github.com/neglectos/ConPan
- *dockerfile_commands.py*: inspects an image in DockerHub and gets its Dockerfile commands with other information like the layers SHA, etc.



