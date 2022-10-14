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

def main():
    pass

if __name__ == "__main__":
    main()
