import config
import sys
import misc
import logging
from PyQt6.QtWidgets import *

configuration = config.Load()
operating_system = configuration['operating_system']
logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()

class ActiveEnvWindow(QDialog):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent=parent

        # We define a few graphical variables from the configuration

        background_color = configuration['child_window_background_color']
        textbox_color = configuration['main_window_textbox_color']
        buttons_color = configuration['buttons_color']
        text_color = configuration['text_color']
        text_font = configuration['text_font']
        text_size = configuration['text_size']

        # Defining our layout variables
        width = 500
        height = 300

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size)

    def initUI(self, background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size):
        self.setWindowTitle('Environment Containers')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Main ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(400, 200)
        self.list_view.itemClicked.connect(self.AllowShell)
        self.list_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Buttons
        self.open_shell_button = QPushButton('Open Shell', self)
        self.open_shell_button.move(40, 240)
        self.open_shell_button.resize(120, 20)
        self.open_shell_button.clicked.connect(self.OpenShell)
        self.open_shell_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.open_shell_button)

        if self.parent is not None:
            self.containers = self.parent.GetRunningScenarioContainers()
            for container in self.containers:
                self.list_view.addItem(f'{container.name} - {container.ports}')

    # endregion

    # region =====Graphical Methods=====

    def DisableButton(self, button : QPushButton):
        buttons_color = configuration['disabled_buttons_color']
        text_color = configuration['disabled_text_color']
        text_font = configuration['text_font']

        button.setEnabled(False)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font};')

    def EnableButton(self, button : QPushButton):
        buttons_color = configuration['buttons_color']
        text_color = configuration['text_color']
        text_font = configuration['text_font']

        button.setEnabled(True)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    def AllowShell(self):
        self.EnableButton(self.open_shell_button)

    def OpenShell(self):
        container_info = self.list_view.currentItem().text().split('-')[0]
        for container in self.containers:
            if container.name in container_info:
                logger.info(f'Opening up a terminal for the {container.name} container.')
                command = f"docker exec -it {container.id} /bin/sh"
                misc.open_terminal(operating_system, command)

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ActiveEnvWindow()
    ex.show()
    sys.exit(app.exec())