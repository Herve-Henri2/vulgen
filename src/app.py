import sys
import os
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
        self.user_input = None

        # We then start initializing our window
        super().__init__()
        self.initUI(background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3)

        # Initializing Docker
        if self.InitializeDocker():
            pass


    def initUI(self, background_color, textbox_color, buttons_color, text_color, text_font, text_size, width, height, col1, col2, col3):

        self.setWindowTitle('Vulnerable Environment Generator')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, 20)
        self.textbox.resize(600,400)
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText("Welcome to our vulnerable environment generator!")
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
                        return
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
                        return
                    if not misc.ProcessRunning('dockerd'):
                        try:
                            self.Write('Starting the docker service, please wait...')
                            os.popen('systemctl start docker')
                            tries += 1
                        except Exception as ex:
                            self.Write(ex)
                            return service_running

    def InitializeDocker(self):

        def DetectDockerDesktopPath():
            possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
            for path in possible_paths:
                if os.path.exists(path):
                    return path

        # Set the "Docker Desktop.exe" path for the Windows users if it hasn't been set yet
        if self.docker_client_path == "" and self.operating_system == "Windows":
            self.docker_client_path = DetectDockerDesktopPath()
            if not self.docker_client_path:
                self.Write('Could not detect Docker Desktop, you need to have it installed to use this application.\n' 
                           'If you did install it, please open up the options window and enter the path of "Docker Desktop.exe".')
                # TODO Handle the input
                # config.Save('docker_desktop', self.docker_client_path)
        if not self.DockerServiceRunning():
            self.Write('Could not launch the docker service.')
            return False
        self.docker_client = docker.from_env()
        return True

    # endregion

    # region =====Graphical Methods=====

    def GetUserInput(self):
        self.user_input = self.entry.text()
        self.entry.setText(" ")

    def closeEvent(self, event):
        widgetList = QApplication.topLevelWidgets()
        numWindows = len(widgetList)
        if numWindows > 1:
            event.accept()
        else:
            event.ignore()

    def setText(self, text):
        self.textbox.setPlainText(text)

    def Write(self, text):
        self.textbox.appendPlainText(text)

    def OpenOptions(self):
        self.options = OptionsWindow()
        self.options.exec()



    # endregion

    # region =====Main Methods=====
            
            

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
