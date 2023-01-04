import os
import config
import logging
import docker
from misc import *
from application import sep, src_folder_path

# Documentation link: https://docker-py.readthedocs.io/en/stable/

# logger
configuration = config.Load()
logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()

def image_in(images, wanted_image_name):
    '''
    Checks whether or not an image list contains a specific image, different from docker_client.images.get(name).
    '''
    for image in images:
        if wanted_image_name in image.tags[0]:
            return True
    return False

def container_in(containers, wanted_container_image_name):
    '''
    Checks whether or not a container list contains a specific container based on the container's image name.
    This function is different from docker_client.containers.get(name) 
    '''
    for container in containers:
        if wanted_container_image_name in container.image.tags[0]:
            return True
    return False

def network_in(networks, wanted_network_name):
    '''
    Checks whether or not a network list contains a specific network based on the network's name.
    This function is different from docker_client.networks.get(name)
    '''
    for network in networks:
        if wanted_network_name in network.name:
            return True
    return False

def get_image(image_name, images=None):
    '''
    Searches for an image in an image list based on the image's name.

    Returns: docker.image object, index of image
    '''
    if images is None:
        docker_client = docker.from_env()
        images = docker_client.images.list()
    for index, image in enumerate(images):
        if image_name in image.tags[0]:
            return image, index
    #print(f"There is no image corresponding to {image_name}")

def get_container(container_image_name, containers=None):
    '''
    Searches for a container object in a container list based on the container's image name.

    Returns: docker.container object, index of container
    '''
    if containers is None:
        docker_client = docker.from_env()
        containers = docker_client.containers.list()
    for index, container in enumerate(containers):
        if container_image_name in container.image.tags[0]:
            return container, index
    #print(f"No {container_image_name} container was found")

def get_network(networks, network_name):
    '''
    Searches for a network object in a network list based on the network's name.
    
    Returns docker.network object, index of network
    '''
    for index, network in enumerate(networks):
        if network_name in network.name:
            return network, index


def GetImages(docker_client=None):
    '''
    Returns a dictionnary listing all the existing docker images on the machine.
    '''
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
    '''
    Returns a dictionnary listing all the docker containers (running or not) on the machine.
    '''
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

def GetCustomImages() -> list[list]:
    '''
    Retrieves all custom images names from the docker_images folder.
    '''
    custom_images_path = src_folder_path + f"{sep}..{sep}docker_images"  # src folder absolute path + path to docker_images from src folder
    base_images_path = custom_images_path + f"{sep}base_images"
    scenario_images_path = custom_images_path + f"{sep}scenario_images"
    misc_images_path = custom_images_path + f"{sep}misc_images"

    base_images = [folder for folder in os.listdir(base_images_path)] 
    scenario_images = [folder for folder in os.listdir(scenario_images_path)]
    misc_images = [folder for folder in os.listdir(misc_images_path)]

    return base_images, scenario_images, misc_images


def GetNetworks(docker_client=None):
    '''
    Returns a dictionnary listing all the docker networks created on the host machine.
    '''
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

def GetImageRequirements(image_name : str, type : str, docker_client=None):
    '''
    Returns a list of paths leading to all the dockerfiles necessary to build the image passed as a parameter.
    ------------
    Parameters:

    image_name : The name of the image we want to build

    type : The image type (either "base", "scenario" or "misc"), used to search the image in the appropriate folder
    '''
    if docker_client is None:
        docker_client = docker.from_env()
    
    # Get Dockerfile path
    custom_images_path = src_folder_path + f"{sep}..{sep}docker_images"  # src folder absolute path + path to docker_images from src folder
    if type == "scenario":
        dockerfile_path = f'{custom_images_path}{sep}scenario_images{sep}{image_name}'
    elif type == "misc":
        dockerfile_path = f'{custom_images_path}{sep}misc_images{sep}{image_name}'
    elif type == "base":
        dockerfile_path = f'{custom_images_path}{sep}base_images{sep}{image_name}'
    else:
        dockerfile_path = f'{custom_images_path}{sep}{image_name}'

    # Get custom image requirements
    built_images = docker_client.images.list()
    required_images = []
    try:
        with open(f"{dockerfile_path}{sep}req.txt", 'r') as requirements:
            for line in requirements:
                if ':' in line and (req := line.strip().split(':'))[0] == "Image":
                    alreadyBuilt = False
                    for built_image in built_images:
                        if req[1] == built_image.tags[0].split(':')[0]:
                            alreadyBuilt = True
                            break
                    if not alreadyBuilt:
                        required_images.append(req[1])
    except Exception as ex:
        logger.error(ex)
    # Create Dockerfiles path list
    dockerfiles_path = []
    for req_image in required_images:
        req_dockerfile_path = f'{custom_images_path}{sep}base_images{sep}{req_image}'
        dockerfiles_path.append(req_dockerfile_path)
    dockerfiles_path.append(dockerfile_path)
    
    return dockerfiles_path

    