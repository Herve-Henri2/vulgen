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

# With PyQt6
def center(self):

    qr = self.frameGeometry()
    cp = self.screen().availableGeometry().center()

    qr.moveCenter(cp)
    self.move(qr.topLeft())

def AsyncTest(self):
    worker = AsyncTask(self.ShowImages)
    self.threads.append(worker)
    self.threads[0].start()

def ShowImages(self, *args, **kwargs):
    self.Clear()
    self.DisableAllButtons(self.options_button)
    if self.DockerInitSuccess():
        self.Write('Images list:')
        images = self.docker_client.images.list()
        for image in images: 
            self.Write(f'{image.short_id.replace("sha256:", "")} - {self.get_image_name(image.tag)}')
    self.EnableAllButtons()

def ShowContainers(self, *args, **kwargs):
    self.Clear()
    self.DisableAllButtons(self.options_button)
    if self.DockerInitSuccess():
        self.Write('Containers list:')
        containers = self.docker_client.containers.list(all=True)
        for container in containers: 
            self.Write(f'{container.name} - {container.short_id} - {self.get_image_name(container.image)} - {container.status}')
    self.EnableAllButtons()

# Check https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/

class AsyncTask(QThread):

    finished = pyqtSignal()
    #error = pyqtSignal(tuple)
    #result = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super(AsyncTask, self).__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        try:
            self.func(*self.args, **self.kwargs)
            #result = self.func(*self.args, **self.kwargs)
            #if result is not None:
                #self.result.emit(result)
        except Exception as ex:
            print(ex)
            #self.error.emit(ex.__str__, ex.__traceback__)
        finally:
            self.finished.emit()

# /!\ Never use that decorator on functions that update the GUI, only on background calculations and processes!
def Asynchronous(func):
    def wrapper(*args, **kwargs):
        worker = AsyncTask(func, *args, **kwargs)
        func.__worker = worker
        worker.start()
    return wrapper

def main():
    pass

if __name__ == "__main__":
    main()
