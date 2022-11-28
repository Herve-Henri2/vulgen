import docker
import os
import sys

from application import * 
from options_window import OptionsWindow
from scenarios_window import ScenariosWindow
from active_env_window import ActiveEnvWindow
from images_window import ImagesWindow
from containers_window import ContainersWindow
from scenarios import *
import config
import docker_utils as dutils
import misc

# TODO Delete all scenario containers after an update

class MainWindow(BaseWindow):

    # region =====Initializing=====

    welcome_text = ("Welcome to our vulnerable environment generator!\n"
                    "To use the application, check out the buttons on the left side.\n\n"
                    "Here is some useful information you need to know:\n"
                    "----------------------------------------------------------------------\n"
                    "* This application is only supported on Linux and Windows distributions (sorry Mac users!) "
                    "If you are using it on a windows machine, you need to have Docker Desktop installed. "
                    "You can check if the application properly detected the executable path in the options window.\n\n"
                    "* You can start testing yourself by clicking on the \"Scenarios\" button, we provide a detailed "
                    "description as well as hints to help you beat each challenge. If you are stuck, you can always check for"
                    " the solution by clicking on the \"Instructions\" button once you have launched the scenario.\n\n"
                    "* The default shortcuts are: \n"
                    "h -> back to home (this layout)\n"
                    "o -> open up the options window\n"
                    "a -> show more details regarding this project's story\n"
                    "s -> open the Scenarios window")

    def __init__(self):

        # Defining our layout variables
        width = 950
        height = 600
        col1 = 0
        col2 = 180 
        col3 = 820

        # Defining other variables
        self.scenario_ui_components = []

        # We then start initializing our window
        super().__init__()
        self.initUI(width, height, col1, col2, col3)

        if not self.DockerServiceRunning():
            self.StartDocker()
        self.Write(self.welcome_text)


    def initUI(self, width, height, col1, col2, col3):

        self.setWindowTitle('Vulnerable Environment Generator')
        self.setFixedSize(width, height)

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, 20)
        self.textbox.resize(600,400)
        self.textbox.setReadOnly(True)

        # Main entry
        self.entry = QLineEdit(self)
        self.entry.move(col2, 450)
        self.entry.resize(600, 30)
        self.entry.setPlaceholderText('Replace this text with your input then press enter')  

        # Buttons
        self.enter_button = QPushButton('Enter', self)
        self.enter_button.move(col2 + 520, 500)
        self.enter_button.resize(80, 20)
        self.enter_button.clicked.connect(self.GetUserInput)
        self.enter_button.setShortcut('Return')

        self.options_button = QPushButton('Options', self)
        self.options_button.move(col3, 20)
        self.options_button.resize(80, 20)
        self.options_button.clicked.connect(self.OpenOptions)
        self.options_button.setShortcut('o')

        self.about_button = QPushButton('About', self)
        self.about_button.move(col3, 60)
        self.about_button.resize(80, 20)
        self.about_button.clicked.connect(self.ShowAbout)
        self.about_button.setShortcut('a')

        self.home_button = QPushButton('Home', self)
        self.home_button.move(col1 + 20, 20)
        self.home_button.resize(140, 20)
        self.home_button.clicked.connect(self.ShowHome)
        self.home_button.setShortcut('h')

        self.manage_images_button = QPushButton('Manage Images', self)
        self.manage_images_button.move(col1 + 20, 60)
        self.manage_images_button.resize(140, 20)
        self.manage_images_button.clicked.connect(self.ManageImages)

        self.manage_containers_button = QPushButton('Manage Containers', self)
        self.manage_containers_button.move(col1 + 20, 100)
        self.manage_containers_button.resize(140, 20)
        self.manage_containers_button.clicked.connect(self.ManageContainers)

        self.scenarios_button = QPushButton('Scenarios', self)
        self.scenarios_button.move(col1 + 20, 140)
        self.scenarios_button.resize(140, 20)
        self.scenarios_button.clicked.connect(self.OpenScenarios)
        self.scenarios_button.setShortcut('s')

        self.test_button = QPushButton('Test', self)
        self.test_button.move(col1 + 20, 200)
        self.test_button.resize(120, 20)
        self.test_button.clicked.connect(self.Test)
        self.test_button.hide()

        # Scenario UI
        self.scenario_label = QLabel('Active scenario', self)
        self.scenario_label.move(col1 + 40, 240)
        self.scenario_ui_components.append(self.scenario_label)

        self.scenario_textbox = QLineEdit(self)
        self.scenario_textbox.move(col1 + 20, 260)
        self.scenario_textbox.resize(120, 20)
        self.scenario_textbox.setReadOnly(True)
        self.scenario_ui_components.append(self.scenario_textbox)

        self.scenario_instructions_button = QPushButton('Instructions', self)
        self.scenario_instructions_button.move(col1 + 20, 300)
        self.scenario_instructions_button.resize(120, 20)
        self.scenario_instructions_button.clicked.connect(self.ShowInstructions)
        self.scenario_ui_components.append(self.scenario_instructions_button)

        self.scenario_containers_button = QPushButton('Containers', self)
        self.scenario_containers_button.move(col1 + 20, 340)
        self.scenario_containers_button.resize(120, 20)
        self.scenario_containers_button.clicked.connect(self.ShowScenarioContainers)
        self.scenario_ui_components.append(self.scenario_containers_button)

        self.exit_scenario_button = QPushButton('Exit', self)
        self.exit_scenario_button.move(col1 + 20, 380)
        self.exit_scenario_button.resize(120, 20)
        self.exit_scenario_button.clicked.connect(self.ExitScenario)
        self.scenario_ui_components.append(self.exit_scenario_button)

        self.HideScenarioUI()

        # Styling and coloring
        self.ImplementTheme()

    # endregion

    # region =====Graphical Methods=====

    def HideScenarioUI(self):
        for component in self.scenario_ui_components:
            component.hide()

    def ShowScenarioUI(self):
        for component in self.scenario_ui_components:
            component.show()
            if isinstance(component, QPushButton):
                self.EnableButton(component)
        if (running_scenario:=self.GetRunningScenario()) is not None:
            self.scenario_textbox.setText(running_scenario.name)

    def GetUserInput(self):
        self.user_input = self.entry.text()
        self.entry.setText(" ")
                             
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

    def Test(self):
        self.Clear()
        for container in self.GetRunningScenarioContainers():
            self.Write(container.name)

    def ShowInstructions(self):
        running_scenario = self.GetRunningScenario()
        self.setText(running_scenario.instructions)
    
    def ShowScenarioContainers(self):
        self.active_env_containers = ActiveEnvWindow(parent=self)
        self.active_env_containers.exec()
        

    # endregion

    # region =====Main Methods=====

    def ScenarioRunning(self):
        '''
        Searches for a ScenarioThread object in the main window threads.
        '''
        for thread in self.threads:
            if isinstance(thread, ScenarioThread):
                return thread

    def GetRunningScenario(self):
        '''
        Returns the current scenario running.
        '''
        if (scenario_thread := self.ScenarioRunning()) is not None:
            return LoadScenario(scenario_thread.scenario_name)

    def GetRunningScenarioContainers(self):
        '''
        Returns a list of all the containers for the current running scenario.
        '''
        container_list = []
        if (scenario := self.GetRunningScenario()) is not None:
            containers = self.docker_client.containers.list()
            for container in containers:
                if scenario.name in container.name:
                    container_list.append(container)
        return container_list
    
    def DockerServiceRunning(self):
        '''
        Checks if docker is running on the local computer.
        '''
        service_running = False

        if operating_system == "Darwin":
            self.Write('This program is not supported on Mac OS.')
            return service_running

        try:
            docker.from_env()
            service_running = True
        except:
            pass
        finally:
            return service_running
 
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

    def StartDocker(self):
        if operating_system == "Windows":
            if docker_desktop != "":
                try:
                    logger.info('Starting Docker Desktop')
                    os.popen(f'{docker_desktop}')
                    misc.unallowWindowOpening('Docker Desktop')
                except Exception as ex:
                    logger.error(ex)
        elif operating_system == "Linux":
            try:
                logger.info('Starting docker')
                os.popen('systemctl start docker')
            except Exception as ex:
                logger.error(ex)

    @CheckForDocker
    def ManageImages(self):
        self.images_window = ImagesWindow(parent=self)
        self.images_window.exec()

    @CheckForDocker
    def ManageContainers(self):
        self.containers_window = ContainersWindow(parent=self)
        self.containers_window.exec()

    @CheckForDocker
    def LaunchScenario(self, scenario : str):
        '''
        Launches the environment linked to a specified scenario.
        '''
        logger.info(f'Launching the {scenario} environment.')
        self.Clear()
        worker = ScenarioThread(scenario)
        worker.update_console.connect(self.Write)
        worker.started.connect(self.DisableAllButtons)
        worker.finished.connect(self.ShowScenarioUI)
        self.threads.append(worker)
        self.threads[-1].start()
        # TODO manage threads

    def ExitScenario(self):
        '''
        Shuts down the actively running environment.
        '''
        scenario = self.GetRunningScenario()
        self.setText(f'Terminated the {scenario.name} environment.')
        logger.info(f'Terminated the {scenario.name} environment.')
        
        # We stop the containers
        containers = self.docker_client.containers.list()
        for container in containers:
            if scenario.name in container.name:
                container.stop()
        # We destroy the thread
        scenario_thread = self.ScenarioRunning()
        self.threads.remove(scenario_thread)
        # We enable all buttons
        self.EnableAllButtons()
        # We hide the scenario UI
        self.HideScenarioUI()
        

class ScenarioThread(QThread):

    update_console = pyqtSignal(str)

    def __init__(self, scenario_name):
        super(ScenarioThread, self).__init__()
        self.scenario_name = scenario_name
        self.docker_client = docker.from_env()

    def run(self):
        scenario = LoadScenario(self.scenario_name)
        self.update_console.emit(f'Launched the {scenario.name} scenario.')
        logger.info(f'Launched the {scenario.name} environment.')

        for index, image in enumerate(scenario.images):
            image_name = image['name']
            image_ports = image['ports']
            if image['is_main'] is True:
                self.LaunchContainer(image_name, main=True, ports=image_ports, name=f'{scenario.name}_main')
            else:
                self.LaunchContainer(image_name, ports=image_ports, name=f'{scenario.name}_{index}')

        self.update_console.emit('------------------------------------------------------------------------------------\n'
                                 '* Click on the Instructions button to get a better scope of what needs to be done.\n'
                                 '* You can interact with all the environment containers by clicking on the Containers button.')
        self.finished.emit()

    def LaunchContainer(self, image_name, main=False, **kwargs):

        images = self.docker_client.images.list()
        containers = self.docker_client.containers.list(all=True)

        # We first check whether the container exists or not
        try:
            container = dutils.get_container(containers, image_name)[0]
        except: 
            container = None

        # If it exists, just start it
        if container:
            container.start()
        # If not, create it from the image, then call this function again
        elif dutils.image_in(images, image_name):
            self.docker_client.containers.create(image_name, **kwargs)
            self.LaunchContainer(image_name, main, **kwargs)
        # Pull the image if necessary, then call this function again
        else:
            self.update_console.emit(f'Pulling the lastest {image_name} image, please wait...')
            self.docker_client.images.pull(image_name)
            while not dutils.image_in(images, image_name):
                images = self.docker_client.images.list()
            self.update_console.emit('Image pulled!')
            self.LaunchContainer(image_name, main, **kwargs) 

    def LaunchContainer2(self, image_name, main=False, **kwargs):
        # 1. Check if the container exists, if yes, launch it
        # 2. If container doesn't exist, check if the image exists, if yes, create a container then call the function again
        # 3. If no image, if dockerfile exists, build it from the dockerfile then call the function again (/!\ create the network)
        # 4. If no dockerfile, if hub name, pull the image then call the function again
        # 5. If no hub name, we cannot do anything, log and write an error

        # /!\ Some db updates will be necessary (for example if there's no image and we create one, we update the name field)
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
