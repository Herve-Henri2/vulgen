import config
import logging
import os

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class BaseWindow(QWidget):

    def __init__(self):
        super().__init__()

    # region =====Graphical Methods=====

    def DisableButton(self, button : QPushButton):
        buttons_color = theme['disabled_buttons_color']
        text_color = theme['disabled_text_color']
        text_font = theme['text_font']

        button.setEnabled(False)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    def DisableButtons(self, *buttons : QPushButton):
        for button in buttons:
            self.DisableButton(button)

    def DisableAllButtons(self, *exceptions : QPushButton):
        for attribute in self.__dict__:
            button = getattr(self, attribute)
            if isinstance(button, QPushButton) and button not in exceptions:
                self.DisableButton(button)

    def EnableButton(self, button : QPushButton):
        buttons_color = theme['buttons_color']
        text_color = theme['text_color']
        text_font = theme['text_font']

        button.setEnabled(True)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    def EnableButtons(self, *buttons):
        for button in buttons:
            self.EnableButton(button)

    def EnableAllButtons(self, *exceptions : QPushButton):
        for attribute in self.__dict__:
            button = getattr(self, attribute)
            if isinstance(button, QPushButton) and button not in exceptions:
                self.EnableButton(button)

    def ShowElements(self, *elements : QWidget):
        for element in elements:
            if isinstance(element, QWidget):
                element.show()

    def HideElements(self, *elements : QWidget):
        for element in elements:
            if isinstance(element, QWidget):
                element.hide()

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def Write(self, text):
        self.textbox.appendPlainText(text)

    def Clear(self):
        self.textbox.clear()

    def ImplementTheme(self, *exceptions, main_window=True):

        if main_window:
            background_color = theme['main_window_background_color']
            self.setStyleSheet(f'background-color: {background_color}')
        else:
            background_color = theme['child_window_background_color']
            self.setStyleSheet(f'background-color: {background_color}')
        textbox_color = theme['main_window_textbox_color']
        buttons_color = theme['buttons_color']
        border_color = theme['border_color']
        text_color = theme['text_color']
        text_font = theme['text_font']
        text_size = theme['text_size']


        for element in self.__dict__:

            element = getattr(self, element)
            if element in exceptions:
                continue

            if isinstance(element, QLabel):
                element.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
            elif isinstance(element, QPushButton):
                element.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
            elif isinstance(element, QLineEdit):
                element.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "{border_color}"')
            elif isinstance(element, QComboBox):
                element.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size}")
            elif isinstance(element, QPlainTextEdit):
                element.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}'")
            elif isinstance(element, QListWidget):
                element.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")
            elif isinstance(element, QTableWidget):
                element.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")
                element.horizontalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")
                element.verticalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")

    # endregion

# Our wide application variables, that are shared between all the windows within our app
configuration = config.Load()
operating_system = configuration['operating_system']
docker_client_path = configuration['docker_desktop']
theme = config.GetTheme(configuration)
docker_client = None
logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()

def DetectDockerDesktopPath(self):
    '''
    Tries to locate the path of the Docker Desktop executable (windows only)
    '''
    global docker_client_path
    
    possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
    for path in possible_paths:
        if os.path.exists(path):
            docker_client_path = path
            config.Save('docker_desktop', path)

if operating_system == "Windows":
    if not configuration['docker_desktop'] or configuration['docker_desktop'] == "":
        DetectDockerDesktopPath()
    else:
        docker_client_path = configuration['docker_desktop']
