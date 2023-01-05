import docker
import os
import sys

from application import * 
from options_window import OptionsWindow
from scenarios_window import ScenariosWindow
from active_env_window import ActiveEnvWindow
from images_window import ImagesWindow
from containers_window import ContainersWindow
from networks_window import NetworksWindow
from scenarios import *
import docker_utils as dutils
import misc

class MainWindow(BaseWindow):

    # region =====Initializing=====

    welcome_text = ("Welcome to our vulnerable environment generator!\n"
                    "To use the application, check out the buttons on the left side.\n\n"
                    "Here is some useful information you need to know:\n"
                    "----------------------------------------------------------------------\n"
                    "* This application is only supported on Linux and Windows distributions (sorry Mac users!) "
                    "If you are using it on a windows machine, you need to have Docker Desktop installed. "
                    "You can check if the application properly detected the executable path in the options window.\n\n"
                    "* You can select the mode (either Education or Challenge) in the options window.\n"
                    "Once you are ready, launch the scenario of your choice by opening the Scenarios window.\n\n"
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

        self.Write(self.welcome_text)


    def initUI(self, width, height, col1, col2, col3):

        self.setWindowTitle('Vulnerable Environment Generator')
        self.setFixedSize(width, height)

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, 20)
        self.textbox.resize(600,400)
        self.textbox.setReadOnly(True)

        # Buttons
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
        
        self.manage_networks_button = QPushButton('Manage Networks', self)
        self.manage_networks_button.move(col1 + 20, 140)
        self.manage_networks_button.resize(140, 20)
        self.manage_networks_button.clicked.connect(self.ManageNetworks)

        self.scenarios_button = QPushButton('Scenarios', self)
        self.scenarios_button.move(col1 + 20, 180)
        self.scenarios_button.resize(140, 20)
        self.scenarios_button.clicked.connect(self.OpenScenarios)
        self.scenarios_button.setShortcut('s')

        # Scenario UI
        self.scenario_label = QLabel('Active scenario', self)
        self.scenario_label.move(col1 + 40, 240)
        self.scenario_ui_components.append(self.scenario_label)

        self.scenario_textbox = QLineEdit(self)
        self.scenario_textbox.move(col1 + 20, 260)
        self.scenario_textbox.resize(120, 20)
        self.scenario_textbox.setReadOnly(True)
        self.scenario_ui_components.append(self.scenario_textbox)

        self.scenario_instructions_button = QPushButton('Goal', self)
        self.scenario_instructions_button.move(col1 + 20, 300)
        self.scenario_instructions_button.resize(120, 20)
        self.scenario_instructions_button.clicked.connect(self.ShowGoal)
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

        if mode == "Education":
            self.exit_scenario_button.move(col1 + 20, 420)
            self.solution_button = QPushButton('Solution', self)
            self.solution_button.move(col1 + 20, 380)
            self.solution_button.resize(120, 20)
            self.solution_button.clicked.connect(self.ShowSolution)
            self.scenario_ui_components.append(self.solution_button)

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

    def ShowGoal(self):
        running_scenario = self.GetRunningScenario()
        self.setText(running_scenario.goal)
    
    def ShowScenarioContainers(self):
        self.active_env_containers = ActiveEnvWindow(parent=self)
        self.active_env_containers.exec()

    def ShowSolution(self):
        running_scenario = self.GetRunningScenario()
        self.setText(running_scenario.solution)
        

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

    @CheckForDocker
    def ManageImages(self):
        self.images_window = ImagesWindow(parent=self)
        self.images_window.exec()

    @CheckForDocker
    def ManageContainers(self):
        self.containers_window = ContainersWindow(parent=self)
        self.containers_window.exec()
        
    @CheckForDocker
    def ManageNetworks(self):
        self.containers_window = NetworksWindow(parent=self)
        self.containers_window.exec()

    @CheckForDocker
    def LaunchScenario(self, scenario_name : str):
        '''
        Launches the environment linked to a specified scenario.
        '''
        logger.info(f'Launching the {scenario_name} environment.')
        self.Clear()
        worker = ScenarioThread(scenario_name, window=self)
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
        for container in self.GetRunningScenarioContainers():
            container.remove(force=True)
        # We destroy the thread
        scenario_thread = self.ScenarioRunning()
        self.threads.remove(scenario_thread)
        # We enable all buttons
        self.EnableAllButtons()
        # We hide the scenario UI
        self.HideScenarioUI()
    
    #endregion        

class ScenarioThread(BaseThread):

    update_console = pyqtSignal(str)

    def __init__(self, scenario_name, window : BaseWindow=None):
        super(ScenarioThread, self).__init__()
        self.scenario_name = scenario_name
        self.window = window
        self.docker_client = docker.from_env()

    def run(self):
        scenario = LoadScenario(self.scenario_name)
        self.window.LaunchWaitingHandler()
        self.update_console.emit(f'Launched the {scenario.name} scenario.')
        logger.info(f'Launched the {scenario.name} environment.')

        # Launching all the scenario containers
        for container in scenario.containers.values():
            self.LaunchContainer(container, stdin_open=True, tty=True)

        # Attaching to a terminal if allowed and necessary
        if configuration['auto_attach'] is True:
            for image_name, container in self.window.GetRunningScenario().containers.items():
                if container.requires_it is False:
                    continue
                try:
                    container = dutils.get_container(image_name)[0]
                except TypeError:
                    container = dutils.get_container(container.name)[0]
                logger.info(f'Attaching the {container.name} container to a new terminal.')
                command = f"docker logs {container.short_id};docker attach {container.short_id}"
                misc.open_terminal(operating_system, command)

        self.update_console.emit('------------------------------------------------------------------------------------\n'
                                 '* Click on the Goal button to get a better scope of what needs to be done.\n'
                                 '* You can interact with all the environment containers by clicking on the Containers button.')
        if mode == "Education":
            self.update_console.emit('* You can click on the Solution button to get access to the exploit steps')
        self.window.RemoveWaitingHandler()
        self.finished.emit()

    def LaunchContainer(self, container : Container, **kwargs):
        # Setting up the container name
        if container.name != "":
            name = container.name
        else:
            name = f"{container.image_name.split(':')[0].split('/')[-1].capitalize()}"
        if self.scenario_name.lower() not in name.lower():
            name = f"{self.scenario_name}-{name}"
        if container.is_main: name += "_main"

        # Forcefully deleting containers with that name to leave room for the new ones
        try:
            if (old_container := self.docker_client.containers.get(name)) is not None:
                old_container.remove(force=True)
        except:
            pass

        # Building all the prerequisite images that don't exist
        if len(container.dockerfile) !=0:
            try:
                dockerfiles_path = dutils.GetImageRequirements(container.image_name.split(':')[0], type="scenario")
                main_image = dockerfiles_path[-1].split(sep)[-1]

                logger.info(f'Started building the {main_image} image.')
              
                for dockerfile_path in dockerfiles_path:
                    if 'scenario' in dockerfile_path:
                        image = container.image_name.split(':')[0]
                    else:
                        image = dockerfile_path.split(sep)[-1]
                    self.update_console.emit(f'Building the {image} image... (May take some time)')
                    logger.info(f'Building the {image} image...')
                    self.docker_client.images.build(path=dockerfile_path, tag=f"{image}:custom", rm=True)
                    logger.info(f'Done!')
            except Exception as ex:
                self.update_console.emit(f'Error: {str(ex)}')
                logger.error(ex)

        # Running the container (if no image was built, downloads it from the container image name)
        try:
            self.update_console.emit(f"Setting up the \"{container.image_name}\" container...")
            logger.info(f"Setting up the \"{container.image_name}\" container...")
            if len(container.networks) == 0:
                # The _container variable is taken from the docker_client while container is a Container object (defined in scenarios.py)
                _container = self.docker_client.containers.run(image=container.image_name, name=name, ports=container.ports,
                detach=True, network_disabled=True, **kwargs)
            else:
                # Creating all the container networks that don't exist
                for network_name in container.networks:
                    if not dutils.network_in(self.docker_client.networks.list(), network_name):
                        logger.info(f'Creating the network {network_name}')
                        self.docker_client.networks.create(network_name, driver="bridge")
                # Running the docker container
                _container = self.docker_client.containers.run(container.image_name, name=name, ports=container.ports, 
                detach=True, network=container.networks[0], **kwargs)
                # Connecting the container to all its other networks
                if len(container.networks) > 1:
                    networks = [network for network in self.docker_client.networks.list() if network.name in container.networks[1:]]
                    for network in networks:
                        logger.info(f'Connecting the container {container.name} to the network {network.name}')
                        network.connect(_container.short_id)
            logger.info(f"Done!")
        except Exception as ex:
            self.update_console.emit(f'Error: {str(ex)}')
            logger.error(ex)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
