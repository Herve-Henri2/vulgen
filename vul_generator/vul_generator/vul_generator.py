import os
import config 
import platform
import psutil
from time import sleep
import win32gui, win32con
import json
import docker

configuration = config.Load()

# General variables
operating_system = configuration['operating_system']
docker_client_path = configuration['docker_desktop']
#docker_client_path = '"C:/Program Files/Docker/Docker/Docker Desktop.exe"' # This is user specific -> to be changed later

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


def LaunchingDockerImage():
    if not DockerServiceRunning():
        print('Could not manage to use the docker service.')
        if operating_system != "Darwin":
            print('Please check that docker is properly installed on your machine. If you are using the Windows OS, you must install the Docker Desktop app.')
        return
    # print('Docker service up and running!')
    client = docker.from_env()
    print(client.images.list())


def HandleUserInput(choice):
    valid_inputs = ['1', '2', '3']
    
    if choice not in valid_inputs:
        choice = input(f"Invalid input, you must enter a number in {valid_inputs}\nYour choice: ")
        HandleUserInput(choice)
    elif choice == '1':
        print("Ok we'll try")
    elif choice == '2':
        print("Let's try!")
        LaunchingDockerImage()
    elif choice == '3':
        print('Okay bye!')

def main():
    Initialize()
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
    main()
