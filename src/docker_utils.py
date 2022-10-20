from curses.ascii import isdigit
import os
import docker
from misc import *

# Documentation link: https://docker-py.readthedocs.io/en/stable/

# General variables
docker_client = None
images = [] # All the docker images on the machine
containers = [] # All the docker containers on the machine


def DockerServiceRunning():
    '''
    Checks if docker is running on the local computer, and tries to launch it if not.
    '''
    service_running = False
    tries = 0

    while not service_running:
        tries += 1
        try:
            docker.from_env()
            service_running = True
            return service_running
        except Exception as ex:
            if tries == 10:
                print(ex)
                break
            if not ProcessRunning('dockerd'):
                try:
                    print('Starting the docker service, please wait...')
                    os.popen('systemctl start docker')
                except Exception as ex:
                    print(ex)
                    return service_running

def InitializeDocker():
    global docker_client_path
    global docker_client

    # Check whether we can use the docker service or not
    if not DockerServiceRunning():
        print('Could not manage to use the docker service.')
        return False
    
    # Start the docker client through the API
    docker_client = docker.from_env()
    return True


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
    print(f"There is no image corresponding to {image_name}")

def get_container(containers, container_image_name):
    '''
    Searches for a container object in a container list based on the container's image name.

    Returns: docker.container object, index of container
    '''
    for index, container in enumerate(containers):
        if container_image_name in container.image.tags[0]:
            return container, index
    print(f"No {container_image_name} container was found")


def DisplayImages():
    global images
    global docker_client

    images = docker_client.images.list()
    
    print('Images list :')
    for index,image in enumerate(images):
        print(f'    {index + 1}: {image.short_id.replace("sha256:", "")} - {image.tags[0]}')
    print('\n')

def DisplayContainers():
    global containers
    global docker_client
    
    containers = docker_client.containers.list(all=True)
    
    print("Containers list :")
    for index,container in enumerate(containers):
        print(f"    {index + 1}: {container.name} - {container.short_id} - {container.image.tags[0]} - {container.status}")
    print('\n')


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
    
    DisplayImages()
    
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
            if choice >= 0 and choice < len(containers):
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
        return docker_client.containers.create(image.tags[0])
    else:
        error("No valid image could be found...")


def RunContainer(method = None):
    '''
    Allows the user to start an existing container or create and run a new one.
    '''
    global containers
    global docker_client
    
    DisplayContainers()
    
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