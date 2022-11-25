import os
import docker
from misc import *
from application import src_folder_path, operating_system

# Documentation link: https://docker-py.readthedocs.io/en/stable/


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


def GetImages(docker_client=None):
    if docker_client is None:
        docker_client = docker.from_env()

    images = docker_client.images.list()
    
    img_dict = {'id':[], 'name':[], 'tag/version':[]}
    for image in images:
        img_dict['id'].append(image.short_id.replace('sha256:', ''))
        try:
            img_name_label = image.tags[0].split(':')
            img_dict['name'].append(img_name_label[0])
            img_dict['tag/version'].append(img_name_label[1])
        except IndexError:
            img_dict['name'] = image.tags
            img_dict['tag/version'] = image.tags
        
    return img_dict
        

def GetContainers(docker_client=None):
    if docker_client is None:
        docker_client = docker.from_env()
    
    containers = docker_client.containers.list(all=True)
    
    cont_dict = {'id':[], 'name':[], 'image':[], 'status':[], 'networks':[]}
    for container in containers:
        cont_dict['id'].append(container.short_id)
        cont_dict['name'].append(container.name)
        cont_dict['image'].append(container.image.tags[0])
        cont_dict['status'].append(container.status)
        
        cont_dict['networks'].append("") # can only work if the container is running
        networks = docker_client.networks.list()
        for network in networks:
            network.reload()
            if container in network.containers:
                cont_dict['networks'][-1] += f"{network.name}, "
        cont_dict['networks'][-1] = cont_dict['networks'][-1][:-2]                
    
    return cont_dict


def GetCustomImages():
    '''
    Retrieves all custom images names from the docker_images folder.
    '''
    to_exclude = ['README.md', 'base_images']
    
    sep = '/' if operating_system == "Linux" else '\\'
    path = src_folder_path + f"{sep}..{sep}docker_images"  # src folder absolute path + path to docker_images from src folder
    custom_images = [folder for folder in os.listdir(path) if folder not in to_exclude]
        
    return custom_images


def GetNetworks(docker_client=None):
    if docker_client is None:
        docker_client = docker.from_env()
    
    networks = docker_client.networks.list()
    network_dict = {'id':[], 'name':[], 'containers':[]}
    for network in networks:
        network.reload() # required to get connected containers (cf. https://github.com/docker/docker-py/issues/1775)
        network_dict['id'].append(network.short_id)
        network_dict['name'].append(network.name)
        network_dict['containers'].append(str(len(network.containers))) # only counts currently running containers
    
    return network_dict
