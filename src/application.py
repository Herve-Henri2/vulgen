import config
import misc
import scenarios
import docker
import logging
import os
import platform
import time
import sys

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

        self.window_type = str(type(self)).replace("<class '", "").replace("'>", "")
        logger.info(f'Instanciating a {self.window_type} object.')
        self.docker_client = None
        self.threads = []
        self.setWindowIcon(QtGui.QIcon(src_folder_path + f"{sep}..{sep}images{sep}shield.png"))
        try: 
            self.docker_client = docker.from_env()
        except:
            pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.info(f'Collapsing the {self.window_type} object.')
        return super().closeEvent(a0)

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
        '''
        Sets the text of the window's textbox to the text passed in as a parameter.
        
        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
        self.textbox.setPlainText(text)

    def Write(self, text):
        '''
        Appends the text passed in as a parameter to the window's textbox.
        
        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
        self.textbox.appendPlainText(text)

    def Clear(self):
        '''
        Clears the window's textbox.
        
        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
        self.textbox.clear()

    def GetText(self):
        '''
        Returns the window's texbox text.
        
        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
        return self.textbox.toPlainText()

    def BorderColorBlink(self):
        '''
        Changes the color of the window's texbox to eiter its original one its background color.\n
        This function is used with the LaunchWaitingHandler() method to not give the user the impression of a freezing app.

        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
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
        '''
        Sets the window's texbox border back to its original color.

        /!\ Only use this function on a window that has a self.textbox : QPlainTextEdit attribute
        '''
        stylesheet_no_border = ';'.join(self.textbox.styleSheet().split(';')[:-1])
        original_stylesheet = f"{stylesheet_no_border}; border: 1px solid '{theme['border_color']}'"
        self.textbox.setStyleSheet(original_stylesheet)

    def ImplementTheme(self, *exceptions, main_window=True):
        '''
        Colors all the window's elements according to the selected theme.
        '''
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
                element.setStyleSheet("QListWidget:item:selected{"
                                      f"background-color: {buttons_color}; color: {text_color}; font-family: {text_font};  border: 1px solid '{border_color}'"
                                      "}"
                                      "QListWidget{"
                                      f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';"
                                      "}")
            elif isinstance(element, QTableWidget):
                element.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")
                element.horizontalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")
                element.verticalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")

    def LaunchWaitingHandler(self):
        '''
        Makes the window's textbox blink, to signal the user that a time consuming process is running.

        /!\ Only use on a window that has a self.texbox : QPlainTextEdit attribute.
        '''
        waiting_handler = WaitingHandler(window=self)
        waiting_handler.blink.connect(self.BorderColorBlink)
        waiting_handler.finished.connect(self.RemoveWaitingHandlerThread)
        waiting_handler.finished.connect(self.OriginalTextboxStyle)
        self.threads.append(waiting_handler)
        self.threads[-1].start()

    def RemoveWaitingHandler(self):
        '''
        Triggers the finished signal of the running WaitingHandler thread object.
        '''
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
    '''
    The goal of this thread object is to make the window's texbox blink while it's running a long process to not give the user
    the impression of freezing.

    /!\ This thread can only be used on a window that has a self.texbox : QPlainTextEdit attribute 
    '''

    blink = pyqtSignal()

    def __init__(self, *args, **kwargs):

        super(WaitingHandler, self).__init__(*args, **kwargs)
        self.stop = False

    def run(self):
        if isinstance(self.window, BaseWindow):
            for attribute in self.window.__dict__:
                if "textbox" not in attribute:
                    continue
                attribute = getattr(self.window, attribute)
                if isinstance(attribute, QPlainTextEdit): 
                    self.Waiting()
                else:
                    logger.error('Cannot run the WaitingHandler object on a window without a self.texbox : QPlainTextEdit attribute')

    def Waiting(self):
        while self.stop is False:
            self.blink.emit()
            # blinking interval (in seconds)
            time.sleep(0.5)
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

def StartDocker():
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

def DockerServiceRunning():
    '''
    Checks if docker is running on the local computer.
    '''
    service_running = False

    if operating_system == "Darwin":
        logger.error('This program is not supported on Mac OS.')
        return service_running

    try:
        docker.from_env()
        service_running = True
    except:
        pass
    finally:
        logger.info(f'Docker service up and running : {service_running}')
        return service_running

def excepthook(exc_type, exc_value, exc_traceback):
    '''
    Allows us to log any exception that will cause the application to crash.
    '''
    import traceback

    # logging
    logger.error("Unhandled exception -> Application Shutdown", exc_info=(exc_type, exc_value, exc_traceback))

    # console printing
    type = str(exc_type).replace("<class '", "").replace("'>", "")
    print(f"Unhandled exception: ")
    traceback.print_tb(exc_traceback, file=sys.stdout)
    print(f"{type}: {exc_value}")

    # closing the app
    sys.exit()

def InitializeApp():
    '''
    Performs all the necessary initializing before launching the main window.
    '''
    sys.excepthook = excepthook

    logger.info('------------------------Application Startup------------------------')

    if operating_system == "Windows":
        if not configuration['docker_desktop'] or configuration['docker_desktop'] == "":
            DetectDockerDesktopPath()
        else:
            docker_desktop = configuration['docker_desktop']

    if not DockerServiceRunning():
        StartDocker()

# endregion

InitializeApp()