from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import config
import sys
import os
import scenarios

class ScenariosWindow(QDialog):

    # region =====Initializing=====

    configuration = config.Load()
    scenarios_db = scenarios.Load()
    scenarios = scenarios_db['scenarios']

    def __init__(self, parent=None):

        self.parent = parent

        # We define a few graphical variables from the configuration

        background_color = self.configuration['child_window_background_color']
        textbox_color = self.configuration['main_window_textbox_color']
        buttons_color = self.configuration['main_window_buttons_color']
        text_color = self.configuration['text_color']
        text_font = self.configuration['text_font']
        text_size = self.configuration['text_size']

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size)


    def initUI(self, background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size):

        self.setWindowTitle('Scenarios')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Side ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(200, 400)
        self.list_view.itemClicked.connect(self.showDetails)
        self.list_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Side TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(240, 20)
        self.textbox.resize(420, 400)
        self.textbox.setReadOnly(True)
        self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Buttons
        self.launch_button = QPushButton('Launch Scenario', self)
        self.launch_button.move(540, 440)
        self.launch_button.resize(120, 20)
        self.launch_button.clicked.connect(self.LaunchScenario)
        self.launch_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        for scenario in self.scenarios:
            self.list_view.addItem(scenario['name'])

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def showDetails(self):
        for scenario in self.scenarios:
            if scenario['name'] == self.list_view.currentItem().text():
                self.setText(scenario['description'])


    # endregion

    # region =====Main Methods=====

    def LaunchScenario(self):
        scenario = self.list_view.currentItem().text()
        self.parent.LaunchScenario(scenario)
        self.close()

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())