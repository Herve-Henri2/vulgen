class BaseThread(QThread):

    def __init__(self, window : BaseWindow=None):
        self.window = window
        self.docker_client = docker.from_env()
        super().__init__()

    def WaitingText(self, str_signal : pyqtSignal(str)):

        dots_number = 3
        text = self.window.GetText()

        while text[-1] == '.':
            text = text[:-1]
        for i in range(dots_number):
            text += '.'
            str_signal.emit(text)
            time.sleep(0.5)
            if i == dots_number - 1:
                text = text[:-dots_number]
                str_signal.emit(text)
                time.sleep(0.5)


class WaitingHandler(QThread):

    update_text = pyqtSignal(str)
    dots_number = 3
    stop = False

    def __init__(self, window : BaseWindow=None):

        self.window = window
        super().__init__()

    def run(self):
        if isinstance(self.window, BaseWindow):
            self.WaitingText()

    def WaitingText(self):
        text = self.window.GetText()
        # Removing all the dots at the end of our text
        while text[-1] == '.':
            text = text[:-1]
        for i in range(self.dots_number):
            text += '.'
            self.update_text.emit(text)
            time.sleep(0.5)
            if i == self.dots_number - 1:
                text = text[:-self.dots_number]
                self.update_text.emit(text)
                time.sleep(0.5)
        if self.stop is True:
            self.finished.emit()
        else:
            # Once done, we call the function again
            self.WaitingText()

def LaunchWaitingHandler(self):
    waiting_handler = WaitingHandler(window=self)
    waiting_handler.update_text.connect(self.setText)
    waiting_handler.finished.connect(self.RemoveWaitingHandlerThread)
    self.threads.append(waiting_handler)
    self.threads[-1].start()

def RemoveWaitingHandler(self):
    for thread in self.threads:
        if isinstance(thread, WaitingHandler):
            thread.stop = True

def RemoveWaitingHandlerThread(self):
    for thread in self.threads:
        if isinstance(thread, WaitingHandler):
            self.threads.remove(thread)

    def LaunchContainer(self, image_name, dockerfile, networks_names, **kwargs):     
        if len(dockerfile) != 0:
            try:
                dockerfiles_path = dutils.GetImageRequirements(image_name.split(':')[0])
                main_image = dockerfiles_path[-1].split(sep)[-1]
                
                self.update_console.emit(f'Started building the {main_image} image.')
                logger.info(f'Started building the {main_image} image.')
                
                for dockerfile_path in dockerfiles_path:
                    image = dockerfile_path.split(sep)[-1]
                    self.update_console.emit(f'Building the {image} image...')
                    logger.info(f'Building the {image} image...')
                    self.docker_client.images.build(path=dockerfile_path, tag=f"{image}:custom", rm=True)
                    logger.info(f'Done!')

            except Exception as ex:
                self.update_console.emit(f'Error: {str(ex)}')
                logger.info(ex)
        
        try:
            self.update_console.emit(f"Setting up the \"{image_name}\" container...")
            logger.info(f"Setting up the \"{image_name}\" container...")
            if len(networks_names) == 0:
                container = self.docker_client.containers.run(image_name, detach=True, network_disabled=True, **kwargs)
            else:
                for network_name in networks_names:
                    if not dutils.network_in(self.docker_client.networks.list(), network_name):
                        self.docker_client.networks.create(network_name, driver="bridge")
                
                container = self.docker_client.containers.run(image_name, detach=True, network=networks_names[0], **kwargs)
                if len(networks_names) > 1:
                    networks = [network for network in self.docker_client.networks.list() if network.name in networks_names[1:]]
                    for network in networks:
                        network.connect(container.short_id)
            logger.info(f"Done!")
        except Exception as ex:
            self.update_console.emit(f'Error: {str(ex)}')
            logger.info(ex)


def GetCustomImages():
    '''
    Retrieves all custom images names from the docker_images folder.
    '''
    to_exclude = ['README.md', 'base_images']
    
    custom_images_path = src_folder_path + f"{sep}..{sep}docker_images"  # src folder absolute path + path to docker_images from src folder
    base_images_path = custom_images_path + f"{sep}base_images"
    
    custom_images = [folder for folder in os.listdir(custom_images_path) if folder not in to_exclude]
    custom_images.extend([f"base_images{sep}{folder}" for folder in os.listdir(base_images_path) if folder not in to_exclude])
        
    return custom_images