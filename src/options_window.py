from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import config
import sys

class OptionsWindow(QDialog):

    # region =====Initializing=====
    configuration = config.Load()

    docker_client_path = configuration['docker_desktop']

    def __init__(self):

        # We define a few graphical variables from the configuration

        background_color = self.configuration['options_window_background_color']
        buttons_color = self.configuration['main_window_buttons_color']
        text_color = self.configuration['text_color']
        text_font = self.configuration['text_font']
        text_size = self.configuration['text_size']

        # Defining our layout variables
        width = 500
        height = 300

        super().__init__()
        self.initUI(background_color, width, height, buttons_color, text_color, text_font, text_size)

    def initUI(self, background_color, width, height, buttons_color, text_color, text_font, text_size):

        self.setWindowTitle('Options')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(380, 260)
        self.save_button.resize(80, 20)
        self.save_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    # endregion



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OptionsWindow()
    ex.show()
    sys.exit(app.exec())