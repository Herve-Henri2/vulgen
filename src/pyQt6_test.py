import sys
import config
from PyQt6.QtWidgets import *
from PyQt6 import QtCore

class MainWindow(QWidget):

    # region =====Initializing=====

    def __init__(self):

        # We first load the graphical parameters from the configuration
        configuration = config.Load()

        # We define a few variables from it
        background_color = configuration['main_window_background_color']
        textbox_color = configuration['main_window_textbox_color']
        buttons_color = configuration['main_window_buttons_color']
        text_color = configuration['text_color']
        text_font = configuration['text_font']
        text_size = configuration['text_size']

        # Defining our layout variables
        width = 950
        height = 600
        col1 = 0; 
        col2 = 180; 
        col3 = 850

        # We then start initializing our window
        super().__init__()

        self.setWindowTitle('Vulnerable environment generator.')
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

    # endregion

    # region =====Graphical Methods=====

    def GetUserInput(self):
        user_input = self.entry.text()
        return user_input

    def setText(self, text):
        self.textbox.setPlainText(text)

    def Write(self, text):
        self.textbox.appendPlainText(text)

    # endregion



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())