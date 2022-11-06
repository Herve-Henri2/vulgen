import docker_functions as df
import sys
import os
import config
import docker
import scenarios
import misc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from options_window import *
from scenarios_window import *



class MainWindow(QWidget):

    # region =====Initializing=====

    # We first load the configuration and define class variables
    configuration = config.Load()
    operating_system = configuration['operating_system']
    docker_client_path = configuration['docker_desktop']
    docker_client = None
    welcome_text = ("Welcome to our vulnerable environment generator!\n"
                    "To use the application, check out the buttons on the left side.\n\n"
                    "Here is some useful information you need to know:\n"
                    "* This application is only supported on Linux and Windows distributions (sorry Mac users!) "
                    "If you are using it on a windows machine, you need to have Docker Desktop installed. "
                    "You can check if the application properly detected the executable path in the options window.\n"
                    "* You can start testing yourself by clicking on the \"Launch Scenario\" button, we provide a detailed "
                    "description as well as hints to help you beat each challenge. If you are stuck, you can always check for"
                    "the solution by [undefined for now].\n"
                    "* The default shortcuts are: \n"
                    "h -> back to home (this layout)\n"
                    "o -> open up the options window\n"
                    "a -> show more details regarding this project's story")

    def __init__(self):

        # We define a few graphical variables from the configuration
        background_color = self.configuration['main_window_background_color']
        textbox_color = self.configuration['main_window_textbox_color']
        buttons_color = self.configuration['main_window_buttons_color']
        text_color = self.configuration['text_color']
        text_font = self.configuration['text_font']
        text_size = self.configuration['text_size']

        # Defining our layout variables
        width = 950
        height = 600
        col1 = 0
        col2 = 180 
        col3 = 820

        # Defining other variables
        self.threads = []

        # We then start initializing our window
        super().__init__()
        self.initUI(background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3)

        if self.operating_system == "Windows" :
            self.DetectDockerDesktopPath()

        if not self.DockerServiceRunning():
            self.StartDocker()
        self.Write(self.welcome_text)


    def initUI(self, background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3):

        self.setWindowTitle('Vulnerable Environment Generator')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color};')

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, 20)
        self.textbox.resize(600,400)
        self.textbox.setReadOnly(True)
        self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Main entry
        self.entry = QLineEdit(self)
        self.entry.move(col2, 450)
        self.entry.resize(600, 30)
        self.entry.setPlaceholderText('Replace this text with your input then press enter')  
        self.entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "#FFFFFF"')

        # Buttons
        self.enter_button = QPushButton('Enter', self)
        self.enter_button.move(col2 + 520, 500)
        self.enter_button.resize(80, 20)
        self.enter_button.clicked.connect(self.GetUserInput)
        self.enter_button.setShortcut('Return')
        self.enter_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.options_button = QPushButton('Options', self)
        self.options_button.move(col3, 20)
        self.options_button.resize(80, 20)
        self.options_button.clicked.connect(self.OpenOptions)
        self.options_button.setShortcut('o')
        self.options_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.about_button = QPushButton('About', self)
        self.about_button.move(col3, 60)
        self.about_button.resize(80, 20)
        self.about_button.clicked.connect(self.ShowAbout)
        self.about_button.setShortcut('a')
        self.about_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.home_button = QPushButton('Home', self)
        self.home_button.move(col1 + 20, 20)
        self.home_button.resize(80, 20)
        self.home_button.clicked.connect(self.ShowHome)
        self.home_button.setShortcut('h')
        self.home_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.show_images_button = QPushButton('Show Images', self)
        self.show_images_button.move(col1 + 20, 60)
        self.show_images_button.resize(100, 20)
        self.show_images_button.clicked.connect(self.ShowImages)
        self.show_images_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.show_containers_button = QPushButton('Show Containers', self)
        self.show_containers_button.move(col1 + 20, 100)
        self.show_containers_button.resize(120, 20)
        self.show_containers_button.clicked.connect(self.ShowContainers)
        self.show_containers_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.scenarios_button = QPushButton('Scenarios', self)
        self.scenarios_button.move(col1 + 20, 140)
        self.scenarios_button.resize(120, 20)
        self.scenarios_button.clicked.connect(self.OpenScenarios)
        self.scenarios_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        self.scenarios_button = QPushButton('Test', self)
        self.scenarios_button.move(col1 + 20, 180)
        self.scenarios_button.resize(120, 20)
        self.scenarios_button.clicked.connect(self.Test)
        self.scenarios_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    # endregion

    # region =====Graphical Methods=====

    def GetUserInput(self):
        self.user_input = self.entry.text()
        self.entry.setText(" ")

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def Clear(self):
        self.textbox.setPlainText("")

    def Write(self, text : str):
        self.textbox.appendPlainText(text)

    def DisableAllButtons(self, *exceptions : QPushButton):
        for attribute in self.__dict__:
            if 'button' in attribute:
                button = getattr(self, attribute)
                if button not in exceptions:
                    button.setEnabled(False)

    def EnableAllButtons(self, *exceptions : QPushButton):
        for attribute in self.__dict__:
            if 'button' in attribute:
                button = getattr(self, attribute)
                if button not in exceptions:
                    button.setEnabled(True)  
                             
    def OpenOptions(self):
        self.options = OptionsWindow(parent=self)
        self.options.exec()

    def ShowAbout(self):
        about_text = ("Coded by ESILV students, this application aims at training and educating yourself in cybersecurity.\n"
                      "With the help of docker containers, vulnerable environments are generated for you to launch an attack or exploit a vulnerability.\n"
                      "The code is open source at github.com/Herve-Henri2/vulgen, under the GPL3 License.")
        self.setText(about_text)

    def ShowHome(self):
        self.setText(self.welcome_text)

    def OpenScenarios(self):
        self.scenarios_window = ScenariosWindow(parent=self)
        self.scenarios_window.exec()


    # endregion

    # region =====Main Methods=====

    def CheckForDocker(func):
        '''
        Decorating function for any method that requires the docker service.
        '''
        def wrapper(self, *args, **kwargs):
            if not self.DockerServiceRunning():
                self.setText('It looks like docker is not running on your machine, please make sure you have docker installed or Docker Desktop if you are on Windows.\n'
                'You may need to save the path your Docker Desktop.exe in the options window then restart the application.')
            else:
                self.docker_client = docker.from_env()
                try:
                    func(self)
                except TypeError:
                    func(self, *args, **kwargs)
        return wrapper

    def DetectDockerDesktopPath(self):
        '''
        Tries to locate the path of the Docker Desktop executable (windows only)
        '''
        possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
        for path in possible_paths:
            if os.path.exists(path):
                self.docker_client_path = path
                config.Save('docker_desktop', path)

    def DockerServiceRunning(self):
        '''
        Checks if docker is running on the local computer.
        '''
        service_running = False

        if self.operating_system == "Darwin":
            self.Write('This program is not supported on Mac OS.')
            return service_running

        try:
            docker.from_env()
            service_running = True
        except:
            pass
        finally:
            return service_running

    def StartDocker(self):
        if self.operating_system == "Windows":
            if self.docker_client_path != "":
                try:
                    os.popen(f'{self.docker_client_path}')
                    misc.unallowWindowOpening('Docker Desktop')
                except Exception as ex:
                    # TODO log it
                    print(ex)
        elif self.operating_system == "Linux":
            try:
                os.popen('systemctl start docker')
            except Exception as ex:
                print(ex)

    @CheckForDocker
    def ShowImages(self):
        images = self.docker_client.images.list()
        self.setText("Images list: ")
        for image in images: 
            self.Write(f'{image.short_id.replace("sha256:", "")} - {df.get_image_name(image.tag)}')

    @CheckForDocker
    def ShowContainers(self):
        containers = self.docker_client.containers.list(all=True)
        self.setText("Containers list: ")
        for container in containers: 
            self.Write(f'{container.name} - {container.short_id} - {df.get_image_name(container.image)} - {container.status}')
        # self.Write(str(len(self.threads)))

    @CheckForDocker
    def LaunchScenario(self, scenario):
        self.Clear()
        worker = ScenarioLauncher(scenario)
        worker.update_console.connect(self.Write)
        worker.started.connect(self.DisableAllButtons)
        worker.finished.connect(self.EnableAllButtons)
        self.threads.append(worker)
        self.threads[-1].start()
        # TODO manage threads

    
    def Test(self):
        pass

class ScenarioLauncher(QThread):

    update_console = pyqtSignal(str)
    operating_system = "Windows"

    def __init__(self, scenario_name):
        super(ScenarioLauncher, self).__init__()
        self.scenario_name = scenario_name
        self.docker_client = docker.from_env()

    def run(self):
        scenario = scenarios.LoadScenario(self.scenario_name)
        self.update_console.emit(f'Launching the scenario {scenario.name}...')

        for index, image in enumerate(scenario.images['other']):
            image_name = image['name']
            image_ports = image['ports']
            self.LaunchContainer(image_name, ports=image_ports, name=f'{scenario.name}_{index}')


        main_image = scenario.images['main']
        image_name = main_image['name']
        image_ports = main_image['ports']
        self.LaunchContainer(image_name, main=True, ports=image_ports, name=f'{scenario.name}_main')
        self.update_console.emit('------------------------------------------------------------\n' + scenario.instructions)
        self.finished.emit()

    def LaunchContainer(self, image_name, main=False, **kwargs):

        images = self.docker_client.images.list()
        containers = self.docker_client.containers.list(all=True)

        # We first check whether the container exists or not
        try:
            container = df.get_container(containers, image_name)[0]
        except: 
            container = None

        # If it exists, just start it
        if container:
            self.update_console.emit(f'Launching the container {image_name}')
            container.start()
            # Eventually open up a shell or browser if it's the main one?
            if main:
                command = f"docker exec -it {container.id} /bin/sh"
                misc.open_terminal(self.operating_system, command)
        # If not, create it from the image, then call this function again
        elif df.image_in(images, image_name):
            self.update_console.emit(f'Creating the {image_name} container...')
            self.docker_client.containers.create(image_name, **kwargs)
            self.LaunchContainer(image_name, main, **kwargs)
        # Pull the image if necessary, then call this function again
        else:
            self.update_console.emit(f'Pulling the lastest {image_name} image, please wait...')
            self.docker_client.images.pull(image_name)
            while not df.image_in(images, image_name):
                images = self.docker_client.images.list()
            self.update_console.emit('Image pulled!')
            self.LaunchContainer(image_name, main, **kwargs)
        

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
