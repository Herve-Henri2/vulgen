import sys
import os

from typer import CallbackParam
import config
import docker
import misc
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from options_window import *

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
        self.function_running = False

        # We then start initializing our window
        super().__init__()
        self.initUI(background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3)

        if self.operating_system == "Windows":
            self.DetectDockerDesktopPath()


    def initUI(self, background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3):

        self.setWindowTitle('Vulnerable Environment Generator')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color};')

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, 20)
        self.textbox.resize(600,400)
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText(self.welcome_text)
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

        self.enter_button = QPushButton('Options', self)
        self.enter_button.move(col3, 20)
        self.enter_button.resize(80, 20)
        self.enter_button.clicked.connect(self.OpenOptions)
        self.enter_button.setShortcut('o')
        self.enter_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

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
        self.show_containers_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

  

    # endregion

    # region =====Graphical Methods=====

    def GetUserInput(self):
        self.user_input = self.entry.text()
        self.entry.setText(" ")

    def setText(self, text : str):
        self.textbox.setPlainText(text)

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


    # endregion

    # region =====Main Methods=====

    def DockerServiceRunning(self):
        '''
        Checks if docker is running on the local computer, and tries to launch it if not.
        '''
        service_running = False
        tries = 0

        if self.operating_system == "Darwin":
            self.Write('This program is not supported on Mac OS.')
            return service_running

        while not service_running:
            try:
                docker.from_env()
                service_running = True
                return service_running
            except Exception as ex:
                if self.operating_system == "Windows":
                    if tries == 10:
                        return service_running
                    if not misc.ProcessRunning('Docker Desktop'):
                        try:
                            self.Write('Starting Docker Desktop, please wait...')
                            os.popen(f'{self.docker_client_path}')
                            misc.unallowWindowOpening('Docker Desktop')
                            tries += 1
                        except Exception as ex:
                            self.Write(ex)
                            return service_running
                elif self.operating_system == "Linux":
                    if tries == 10:
                        return service_running
                    if not misc.ProcessRunning('dockerd'):
                        try:
                            self.Write('Starting the docker service, please wait...')
                            os.popen('systemctl start docker')
                            tries += 1
                        except Exception as ex:
                            self.Write(ex)
                            return service_running

    def DetectDockerDesktopPath(self):
        '''
        Tries to locate the path of the Docker Desktop executable (windows only)
        '''
        possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
        for path in possible_paths:
            if os.path.exists(path):
                self.docker_client_path = path
                config.Save('docker_desktop', path)

    def DockerInitSuccess(self):

        # Set the "Docker Desktop.exe" path for the Windows users if it hasn't been set yet
        if self.docker_client_path == "" and self.operating_system == "Windows":
            self.Write('Could not detect Docker Desktop, you need to have it installed to use this application.\n' 
                        'If you did install it, please open up the options window and enter the path of "Docker Desktop.exe".')
            return False
        if not self.DockerServiceRunning():
            self.Write('Could not launch the docker service.')
            return False
        self.docker_client = docker.from_env()
        return True            
            
    def ShowImages(self):
        if self.DockerInitSuccess():
            print('nice!')
    
    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
