import config
import scenarios
import docker
import logging
import os
import platform
import time

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui

# Our wide application variables, that are shared between all the windows within our app
sep = '/' if platform.system() == "Linux" else '\\'
src_folder_path = os.path.realpath(os.path.dirname(__file__))

configuration = config.Load()
scenarios_db = scenarios.Load()
operating_system = configuration['operating_system']
docker_desktop = configuration['docker_desktop']
mode = configuration['modes'][configuration['current_mode_index']]
theme = config.GetTheme(configuration)
logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()


# region =====Base Classes=====

class BaseWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.docker_client = None
        self.threads = []
        self.setWindowIcon(QtGui.QIcon(src_folder_path + f"{sep}..{sep}images{sep}shield.png"))
        try: 
            self.docker_client = docker.from_env()
        except:
            pass

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

    def GetText(self):
        return self.textbox.toPlainText()

    def BorderColorBlink(self):

        border_color = theme['border_color']
        textbox_color = theme['main_window_textbox_color']

        textbox_stylesheet = self.textbox.styleSheet()
        stylesheet_no_border = ';'.join(textbox_stylesheet.split(';')[:-1])
        
        current_border_color = textbox_stylesheet.split(';')[-1].strip()[-8:].replace("'", "")
        if current_border_color == border_color:
            new_border_color = textbox_color
        else:
            new_border_color = border_color
        textbox_stylesheet = f"{stylesheet_no_border}; border: 1px solid '{new_border_color}'"
        self.textbox.setStyleSheet(textbox_stylesheet)

    def OriginalTextboxStyle(self): 
        stylesheet_no_border = ';'.join(self.textbox.styleSheet().split(';')[:-1])
        original_stylesheet = f"{stylesheet_no_border}; border: 1px solid '{theme['border_color']}'"
        self.textbox.setStyleSheet(original_stylesheet)

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

    def LaunchWaitingHandler(self):
        waiting_handler = WaitingHandler(window=self)
        waiting_handler.blink.connect(self.BorderColorBlink)
        waiting_handler.finished.connect(self.RemoveWaitingHandlerThread)
        waiting_handler.finished.connect(self.OriginalTextboxStyle)
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
    # endregion

class BaseThread(QThread):

    def __init__(self, window : BaseWindow=None):

        super().__init__()
        self.window = window
        self.docker_client = docker.from_env()

class WaitingHandler(BaseThread):

    blink = pyqtSignal()

    def __init__(self, *args, **kwargs):

        super(WaitingHandler, self).__init__(*args, **kwargs)
        self.stop = False

    def run(self):
        if isinstance(self.window, BaseWindow):
            self.Waiting()

    def Waiting(self):
        if self.stop is False:
            self.blink.emit()
            time.sleep(0.5)
            self.Waiting()
        else:
            self.finished.emit()

# endregion

# region =====Initializing functions=====

def DetectDockerDesktopPath():
    '''
    Tries to locate the path of the Docker Desktop executable (windows only)
    '''
    global docker_desktop
    
    possible_paths = ['C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe', 'C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe']
    for path in possible_paths:
        if os.path.exists(path):
            docker_desktop = path
            config.Save('docker_desktop', path)

def InitializeApp():
    if operating_system == "Windows":
        if not configuration['docker_desktop'] or configuration['docker_desktop'] == "":
            DetectDockerDesktopPath()
        else:
            docker_desktop = configuration['docker_desktop']

# endregion

InitializeApp()