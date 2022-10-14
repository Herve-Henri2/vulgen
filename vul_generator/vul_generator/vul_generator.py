from importlib.metadata import entry_points
import os, subprocess
import config 
import psutil
import win32gui
import docker
import win32com.client

# Documentation link: https://docker-py.readthedocs.io/en/stable/

configuration = config.Load()

# General variables
operating_system = configuration['operating_system']
docker_client_path = configuration['docker_desktop']
images = []

def Initialize():
    global docker_client_path

    if docker_client_path == "" and operating_system == "Windows":
        docker_client_path = input("Please enter your Docker Desktop.exe file path: ")
        while not os.path.exists(docker_client_path) or "Docker Desktop.exe" not in docker_client_path:
            docker_client_path = input("Path not valid, please enter your Docker Desktop.exe file path: ")
        config.Save('docker_desktop', docker_client_path)

def ProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def unallowWindowOpening(window_name, done=False):
    '''
    Waits for the specified window to open up to immediately close it.
    '''
    while not done:
        foreground_window = win32gui.GetForegroundWindow()
        if win32gui.GetWindowText(foreground_window) == window_name:
            win32gui.ShowWindow(foreground_window, False)
            done = True

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
                if not ProcessRunning('Docker Desktop'):
                    try:
                        print('Starting Docker Desktop, please wait...')
                        os.popen(f'{docker_client_path}')
                        unallowWindowOpening('Docker Desktop')
                    except Exception as ex:
                        print(ex)
                        return service_running
            elif operating_system == "Linux":
                if not ProcessRunning('docker'):
                    try:
                        print('Starting the docker service, please wait...')
                        os.popen('sudo systemctl start docker')
                    except Exception as ex:
                        print(ex)
                        return service_running

def image_in(images, wanted_image_name):
    for image in images:
        image_name = get_image_name(image.tag)
        if wanted_image_name in image_name:
            return True
    return False

def get_image_name(image_tag):
    image_tag=str(image_tag)
    return image_tag.replace("<bound method Image.tag of <Image: '", '').replace("'>>", '')

def LaunchingDockerImage():
    if not DockerServiceRunning():
        print('Could not manage to use the docker service.')
        if operating_system != "Darwin":
            print('Please check that docker is properly installed on your machine. If you are using the Windows OS, you must install the Docker Desktop app.')
        return
    # print('Docker service up and running!')
    client = docker.from_env()
    global images 
    images = client.images.list()

    #print("Here are all your available images:")
    #print(images)
    if image_in(images, "ubuntu"):
        print('Starting the ubuntu container as an interactive bash...')
        #client.containers.run('ubuntu')
        #client.containers.run('ubuntu', entrypoint="bin/bash", detach=True, tty=True)
        WshShell = win32com.client.Dispatch("WScript.Shell")
        WshShell.run("docker run -it --entrypoint /bin/bash ubuntu") 
    else:
        choice = input('Looks like you do not have an ubuntu image, do you want to pull it from the Hub? (y/n) : ')
        while choice != "y" and choice !="n":
            choice = input('You must enter either y or n: ')
        if choice == "y":
            print('Pulling the latest ubuntu image, please wait...')
            client.images.pull('ubuntu')
            while not image_in(images, "ubuntu"):
                images = client.images.list()
            print('Image pulled!')
            LaunchingDockerImage()
        if choice == "n":
            print('Going back to the main menu\n')
            main()


def HandleUserInput(choice):
    valid_inputs = ['1', '2', '3']
    
    if choice not in valid_inputs:
        choice = input(f"Invalid input, you must enter a number in {valid_inputs}\nYour choice: ")
        HandleUserInput(choice)
    elif choice == '1':
        print("Not implemented for now!")
    elif choice == '2':
        LaunchingDockerImage()
    elif choice == '3':
        print('Okay bye!')

def main():
    choice = input('------------------------------------------------\n'
                   'Welcome to our vulnerable environment generator!\n'
                   '------------------------------------------------\n'
                   'What do you wish to do?\n'
                   '1: Create a DockerFile\n'
                   '2: Generate Ubuntu docker container\n'
                   '3: Exit\n'
                   '------------------------------------------------\n'
                   'Your choice: ')
    HandleUserInput(choice)

if __name__ == "__main__":
    Initialize()
    main()
