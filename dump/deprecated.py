# File where we dump all our old functions we do not need anymore but may want to save for some reason.


def DockerServiceRunning():
    '''
    Check if the docker daemon is up and running.
    '''
    service_running = False

    if operating_system == "Darwin":
        print('This program is not supported on Mac OS.')
        return service_running

    while not service_running:
        if operating_system == "Windows":
            if ProcessRunning('Docker Desktop'):
                service_running = True
                return service_running
            else:
                try:
                    print('Starting Docker Desktop, please wait...')
                    os.popen(f'{docker_client_path}')
                except Exception as ex:
                    print(ex)
                    return service_running
        elif operating_system == "Linux":
            if ProcessRunning('docker'):
                service_running = True
                return service_running
            else:
                try:
                    print('Starting the docker service, please wait...')
                    os.popen('sudo systemctl start docker')
                except Exception as ex:
                    print(ex)
                    return service_running

def Log4Shell():
    subprocess.call(
                "docker run --name CVE-2021-44228 -dp 8080:8080 ghcr.io/christophetd/log4shell-vulnerable-app@sha256:6f88430688108e512f7405ac3c73d47f5c370780b94182854ea2cddc6bd59929",
                shell=True,
            )

def LaunchUbuntuContainer():

    global docker_client
    global images 
    global containers

    images = docker_client.images.list()
    containers = docker_client.containers.list(all=True)

    try:
        ubuntu_container = get_container(containers, "ubuntu")[0]
    except: 
        ubuntu_container = None

    if ubuntu_container:
        print('Starting the ubuntu container as an interactive bash...\n')
        ubuntu_container.start()
        command = f"docker exec -it {ubuntu_container.id} /bin/bash"
        misc.open_terminal(operating_system, command)      
        main()

    if image_in(images, "ubuntu"):
        print('Creating ubuntu container and starting an interactive bash...\n')
        command = "docker run -it --entrypoint /bin/bash ubuntu"
        misc.open_terminal(operating_system, command)
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
            LaunchUbuntuContainer()
        if choice == "n":
            print('Going back to the main menu\n')
            main()

def main():
    pass

if __name__ == "__main__":
    main()
