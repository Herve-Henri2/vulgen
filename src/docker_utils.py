from curses.ascii import isdigit
from distutils.sysconfig import customize_compiler
import os
import docker
from misc import *

# Documentation link: https://docker-py.readthedocs.io/en/stable/

# General variables
docker_client = None
images = [] # All the docker images on the machine
containers = [] # All the docker containers on the machine


def image_in(images, wanted_image_name):
    '''
    Checks whether or not an image list contains a specific image.
    '''
    for image in images:
        if wanted_image_name in image.tags[0]:
            return True
    return False

def container_in(containers, wanted_container_image_name):
    '''
    Checks whether or not a container list contains a specific container based on the container's image name.
    '''
    for container in containers:
        if wanted_container_image_name in container.image.tags[0]:
            return True
    return False

def get_image(images, image_name):
    '''
    Searches for an image in an image list based on the image's name.

    Returns: docker.image object, index of image
    '''
    for index, image in enumerate(images):
        if image_name in image.tags[0]:
            return image, index
    #print(f"There is no image corresponding to {image_name}")

def get_container(containers, container_image_name):
    '''
    Searches for a container object in a container list based on the container's image name.

    Returns: docker.container object, index of container
    '''
    for index, container in enumerate(containers):
        if container_image_name in container.image.tags[0]:
            return container, index
    #print(f"No {container_image_name} container was found")


def GetImages():
    global images
    global docker_client

    images = docker_client.images.list()
    
    img_dict = {'id':[], 'name':[], 'tag/version':[]}
    for image in images:
        img_dict['id'].append(image.short_id.replace('sha256:', ''))
        img_name_label = image.tags[0].split(':')
        img_dict['name'].append(img_name_label[0])
        img_dict['tag/version'].append(img_name_label[1])
        
    return img_dict
        

def GetContainers():
    global containers
    global docker_client
    
    containers = docker_client.containers.list(all=True)
    
    cont_dict = {'id':[], 'name':[], 'image':[], 'status':[]}
    for container in containers:
        cont_dict['id'].append(container.short_id)
        cont_dict['name'].append(container.name)
        cont_dict['image'].append(container.image.tags[0])
        cont_dict['status'].append(container.status)
    
    return cont_dict


def GetCustomImages():
    '''
    Retrieve all custom images names from the docker_images folder.
    '''
    to_exclude = ('README.md', 'base_images')
    
    path = os.path.realpath(os.path.dirname(__file__)) + "/../docker_images"  # src folder absolute path + path to docker_images from src folder
    custom_images = [folder for folder in os.listdir(path) if folder not in to_exclude]
    
    img_list = []
    for i in range(len(custom_images)):
        img_list.append(custom_images[i])
        
    return img_list


def FetchImage():
    '''
    Pulls a new Docker image.
    '''
    img_name = input("Enter the name of the image you wish to download :\n")
    img_tag = ""
    image = ""
    
    latest = input("Do you want the latest version ? (y/n)")
    while latest not in ["y", "n"]:
        latest = input('You must enter either y or n: ')
    if latest == "y":
        image = f"{img_name}"
    elif latest == "n":
        img_tag = input("Enter the tag for the image you want to download :\n")
        image = f"{img_name}:{img_tag}"
    
    return docker_client.images.pull(image)


def CreateContainer():
    '''
    Allows the user to create a new container.
    
    Returns: docker.container object
    '''
    global images
    global docker_client
    
    GetImages()
    
    choice = None
    image = None
    
    while(choice == None):
        print("You can create a new container from an existing image by entering the image index.")
        print("Alternatively you can create a container from a new image by entering 'new'.")
        print("Enter 'exit' to return to the menu.\n")
        choice = input("\n> ").lower()

        if choice == "new":
            image = FetchImage()
        elif choice.isdigit():
            choice = int(choice) - 1
            if choice >= 0 and choice < len(images):
                image = images[choice]
            else:
                error("Your choice is out of range...")
                choice = None
        elif choice == "exit":
            return
        else:
            error("Invalid input...")
            choice = None
    
    if image != None:
        return docker_client.containers.create(image.tags[0], stdin_open=True, tty=True) #stdion_open and tty = True <=> docker create -it
    else:
        error("No valid image could be found...")


def RunContainer(method = None):
    '''
    Allows the user to start an existing container or create and run a new one.
    '''
    global containers
    global docker_client
    
    GetContainers()
    
    choice = None
    container = None
    
    while(choice == None):
        print("You can start an existing container by entering its index.")
        print("Alternatively you can create and run a new container by entering 'new'.")
        print("Enter 'exit' to return to the menu.\n")
        choice = input("\n> ").lower()

        if choice == "new":
            container = CreateContainer()
        elif choice.isdigit():
            choice = int(choice) - 1
            if choice >= 0 and choice < len(containers):
                container = containers[choice]
            else:
                error("Your choice is out of range...")
                choice = None
        elif choice == "exit":
            return
        else:
            error("Invalid input...")
            choice = None
    
    if container != None:
        if method == None:
            command = f"docker start -i {container.id}"
        elif method == "bash":
            container.start()
            command = f"docker exec -it {container.id} /bin/bash"
        open_terminal(command)
    else:
        error("No valid container could be found...")