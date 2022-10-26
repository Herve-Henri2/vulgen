import os
import config 
import misc
import docker 
import subprocess

# Documentation link: https://docker-py.readthedocs.io/en/stable/
configuration = config.Load()

# General variables
operating_system = configuration['operating_system']
docker_client_path = configuration['docker_desktop'] # For Windows OS only
docker_client = None
images = [] # All the docker images on the machine
containers = [] # All the docker containers on the machine

def DockerServiceRunning():
    '''
    Checks if docker is running on the local computer, and tries to launch it if not.
    '''
    service_running = False
    tries = 0

    if operating_system == "Darwin":
        print('This program is not supported on Mac OS.')
        return service_running

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
            if operating_system == "Windows":
                if not misc.ProcessRunning('Docker Desktop'):
                    try:
                        print('Starting Docker Desktop, please wait...')
                        os.popen(f'{docker_client_path}')
                        misc.unallowWindowOpening('Docker Desktop')
                    except Exception as ex:
                        print(ex)
                        return service_running
            elif operating_system == "Linux":
                if not misc.ProcessRunning('dockerd'):
                    try:
                        print('Starting the docker service, please wait...')
                        os.popen('systemctl start docker')
                    except Exception as ex:
                        print(ex)
                        return service_running

def InitializeDocker():
    global docker_client_path
    global docker_client

    def DetectDockerDesktopPath():
        possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
        for path in possible_paths:
            if os.path.exists(path):
                return path

    # Set the "Docker Desktop.exe" path for the Windows users if it hasn't been set yet
    if docker_client_path == "" and operating_system == "Windows":
        docker_client_path = DetectDockerDesktopPath()
        if not docker_client_path:
            docker_client_path = input("Please enter your Docker Desktop.exe file path: ")
            while not os.path.exists(docker_client_path) or "Docker Desktop.exe" not in docker_client_path:
                docker_client_path = input("Path not valid, please enter your Docker Desktop.exe file path: ")
        config.Save('docker_desktop', docker_client_path)
    # Check whether we can use the docker service or not
    if not DockerServiceRunning():
        print('Could not manage to use the docker service.')
        if operating_system != "Darwin":
            print('Please check that docker is properly installed on your machine. If you are using the Windows OS, you must install the Docker Desktop app.'
            'You can also try to launch Docker Desktop separately from this program.')
        return False
    # Start the docker client through the API
    docker_client = docker.from_env()
    return True

def get_image_name(image_tag):
    image_tag=str(image_tag)
    return image_tag.replace("<bound method Image.tag of <Image: '", '').replace("'>>", '').replace("<Image: '",'').replace("'>", '')

def image_in(images, wanted_image_name):
    '''
    Checks whether or not an image list contains a specific image.
    '''
    for image in images:
        image_name = get_image_name(image.tag)
        if wanted_image_name in image_name:
            return True
    return False

def container_in(containers, wanted_container_image_name):
    '''
    Checks whether or not a container list contains a specific container based on the container's image name.
    '''
    for container in containers:
        container_image_name = get_image_name(container.image)
        if wanted_container_image_name in container_image_name:
            return True
    return False

def get_image(images, image_name):
    '''
    Searches for an image in an image list based on the image's name.

    Returns: docker.image object
    '''
    if not image_in(images, image_name):
        #print(f"There is no image corresponding to {image_name}")
        return
    for index, image in enumerate(images):
        if image_name in get_image_name(image.tag):
            return image, index

def get_container(containers, container_image_name):
    '''
    Searches for a container object in a container list based on the container's image name.

    Returns: docker.container object
    '''
    if not container_in(containers, container_image_name):
        #print(f"No {container_image_name} container was found")
        return
    for index, container in enumerate(containers):
        if container_image_name in get_image_name(container.image):
            return container, index

def LaunchContainer(image_name, **kwargs):
    '''
    Launches a container and opens up a terminal to interact with it.
    ---------------
    Parameters:

    image_name: str
    The image to start or run

    **kwargs: any
    The same arguments as the ones for docker run
    '''
    global docker_client
    global images 
    global containers

    images = docker_client.images.list()
    containers = docker_client.containers.list(all=True)

    # We first check whether the container exists or not
    try:
        container = get_container(containers, image_name)[0]
    except: 
        container = None

    # If it exists, just start it then open up an interactive shell
    if container:
        print(f'Starting the {image_name} container as an interactive bash.\n')
        container.start()
        command = f"docker exec -it {container.id} /bin/sh"
        misc.open_terminal(operating_system, command)      
        main()
    # If not, create it from the image, then call this function again
    elif image_in(images, image_name):
        print(f'Creating the {image_name} container...')
        docker_client.containers.create(image_name, **kwargs)
        LaunchContainer(image_name, **kwargs)
    # Pull the image if necessary, then call this function again
    else:
        choice = input(f'Looks like you do not have a(n) {image_name} image, do you want to pull it? (y/n) : ')
        while choice != "y" and choice !="n":
            choice = input('You must enter either y or n: ')
        if choice == "y":
            print(f'Pulling the latest {image_name} image, please wait...')
            docker_client.images.pull(image_name)
            while not image_in(images, image_name):
                images = docker_client.images.list()
            print('Image pulled!')
            LaunchContainer(image_name, **kwargs)
        if choice == "n":
            print('Going back to the main menu\n')
            main()

def DisplayImages():
    global images
    global docker_client
    print('Image list:')

    images = docker_client.images.list()
    for image in images:
        print(f'{image.short_id.replace("sha256:", "")} - {get_image_name(image.tag)}')
    print('\n')
    main()

def DisplayContainers():
    global containers
    global docker_client
    print('Container list:')

    containers = docker_client.containers.list(all=True)
    for container in containers:
        print(f'{container.name} - {container.short_id} - {get_image_name(container.image)} - {container.status}')
    print('\n')
    main()

def HandleUserInput(choice):
    valid_inputs = ['1', '2', '3', '4', '5']
    
    if choice not in valid_inputs:
        choice = input(f"Invalid input, you must enter a number in {valid_inputs}\nYour choice: ")
        HandleUserInput(choice)
    elif choice == '1':
        LaunchContainer('ubuntu')
    elif choice == '2':
        DisplayImages()
    elif choice == '3':
        DisplayContainers()
    elif choice == '4':
        LaunchContainer("ghcr.io/christophetd/log4shell-vulnerable-app", ports={"8080/tcp":8080}, name="CVE-2021-44228")
    elif choice == '5':
        print('Okay bye!')
        

def main():
    choice = input('------------------------------------------------\n'
                   'Vulnerable environment generator main menu\n'
                   '------------------------------------------------\n'
                   'What do you wish to do?\n'
                   '1: Generate or start ubuntu container\n'
                   '2: Display Image list\n'
                   '3: Display Container list\n'
                   '4: Try Log4shell\n'
                   '5: Exit\n'
                   '------------------------------------------------\n'
                   'Your choice: ')
    HandleUserInput(choice)

if __name__ == "__main__":
    if InitializeDocker():
        main()

