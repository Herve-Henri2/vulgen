from email import message
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import config
import sys
import os

class OptionsWindow(QDialog):

    # region =====Initializing=====

    configuration = config.Load()
    operating_system = configuration['operating_system']
    docker_client_path = configuration['docker_desktop']

    def __init__(self, parent=None):

        self.parent = parent

        # We define a few graphical variables from the configuration

        background_color = self.configuration['options_window_background_color']
        textbox_color = self.configuration['main_window_textbox_color']
        buttons_color = self.configuration['main_window_buttons_color']
        text_color = self.configuration['text_color']
        text_font = self.configuration['text_font']
        text_size = self.configuration['text_size']

        # Defining our layout variables
        width = 500
        height = 300

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size)

    def initUI(self, background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size):

        self.setWindowTitle('Options')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')
        

        # Docker Desktop file path

        self.docker_path_label = QLabel('Docker Desktop path (Windows Only)', self)
        self.docker_path_label.move(50, 20)
        self.docker_path_label.resize(400, 20)
        self.docker_path_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}; font-size: {text_size}')
        
        self.docker_desktop_entry = QLineEdit(self.docker_client_path, self)
        self.docker_desktop_entry.move(50, 40)
        self.docker_desktop_entry.resize(400, 20)
        self.docker_desktop_entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size}; border: 0px')
        if self.operating_system != "Windows":
            self.docker_desktop_entry.setEnabled(False)
        

        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(370, 260)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.Save)
        self.save_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

    # endregion

    # region =====Graphical Methods=====

    # endregion

    def Save(self):

        allowed_to_close = True

        # We check that the docker path entered is correct
        if self.configuration['docker_desktop'] == "" and self.operating_system == "Windows":
            if not os.path.exists(self.docker_desktop_entry.text()) or "Docker Desktop.exe" not in self.docker_desktop_entry.text():
                messagebox = QMessageBox(self)
                messagebox.resize(200, 200)
                messagebox.setText("The docker")
                messagebox.setStyleSheet('background-color: white')
                messagebox.exec()
                allowed_to_close = False
        if allowed_to_close:
            self.close()

    # region =====General Methods=====

    #endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OptionsWindow()
    ex.show()
    sys.exit(app.exec())