import os
import config 
import misc
import docker
import win32com.client

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

    if operating_system == "Darwin":
        print('This program is not supported on Mac OS.')
        return service_running

    while not service_running:
        try:
            docker.from_env()
            service_running = True
            return service_running
        except:
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
                if not misc.ProcessRunning('docker'):
                    try:
                        print('Starting the docker service, please wait...')
                        os.popen('sudo systemctl start docker')
                    except Exception as ex:
                        print(ex)
                        return service_running

def InitializeDocker():
    global docker_client_path
    global docker_client

    # Set the "Docker Desktop.exe" path for the Windows users if it hasn't been set yet
    if docker_client_path == "" and operating_system == "Windows":
        docker_client_path = input("Please enter your Docker Desktop.exe file path: ")
        while not os.path.exists(docker_client_path) or "Docker Desktop.exe" not in docker_client_path:
            docker_client_path = input("Path not valid, please enter your Docker Desktop.exe file path: ")
        config.Save('docker_desktop', docker_client_path)
    # Check whether we can use the docker service or not
    if not DockerServiceRunning():
        print('Could not manage to use the docker service.')
        if operating_system != "Darwin":
            print('Please check that docker is properly installed on your machine. If you are using the Windows OS, you must install the Docker Desktop app.')
        return False
    # Start the docker client through the API
    docker_client = docker.from_env()
    return True

def image_in(images, wanted_image_name):
    for image in images:
        image_name = get_image_name(image.tag)
        if wanted_image_name in image_name:
            return True
    return False

def get_image_name(image_tag):
    image_tag=str(image_tag)
    return image_tag.replace("<bound method Image.tag of <Image: '", '').replace("'>>", '').replace("<Image: '",'').replace("'>", '')

def LaunchingDockerImage():
    # print('Docker service up and running!')
    global images 
    global docker_client

    images = docker_client.images.list()

    #print("Here are all your available images:")
    #print(images)
    if image_in(images, "ubuntu"):
        print('Starting the ubuntu container as an interactive bash...\n')
        #client.containers.run('ubuntu', entrypoint="bin/bash", detach=True, tty=True)
        WshShell = win32com.client.Dispatch("WScript.Shell")
        WshShell.run("docker run -it --entrypoint /bin/bash ubuntu")
        main()
    else:
        choice = input('Looks like you do not have an ubuntu image, do you want to pull it from the Hub? (y/n) : ')
        while choice != "y" and choice !="n":
            choice = input('You must enter either y or n: ')
        if choice == "y":
            print('Pulling the latest ubuntu image, please wait...')
            docker_client.images.pull('ubuntu')
            while not image_in(images, "ubuntu"):
                images = docker_client.images.list()
            print('Image pulled!')
            LaunchingDockerImage()
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
        print(f'{container.short_id} - {get_image_name(container.image)} - {container.status}')
    print('\n')
    main()

def HandleUserInput(choice):
    valid_inputs = ['1', '2', '3', '4']
    
    if choice not in valid_inputs:
        choice = input(f"Invalid input, you must enter a number in {valid_inputs}\nYour choice: ")
        HandleUserInput(choice)
    elif choice == '1':
        LaunchingDockerImage()
    elif choice == '2':
        DisplayImages()
    elif choice == '3':
        DisplayContainers()
    elif choice == '4':
        print('Okay bye!')
        

def main():
    choice = input('------------------------------------------------\n'
                   'Vulnerable environment generator main menu\n'
                   '------------------------------------------------\n'
                   'What do you wish to do?\n'
                   '1: Generate or start Ubuntu docker container\n'
                   '2: Display Image list\n'
                   '3: Display Container list\n'
                   '4: Exit\n'
                   '------------------------------------------------\n'
                   'Your choice: ')
    HandleUserInput(choice)

if __name__ == "__main__":
    if InitializeDocker():
        main()
