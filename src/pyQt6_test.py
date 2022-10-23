import sys
import config
from PyQt6.QtWidgets import *
from PyQt6 import QtCore

class MainWindow(QWidget):

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
        col2 = 150; col2_row1 = 0; col2_row2 = 20; col2_row3 = 520; col2_row4 = 540
        col3 = 850

        # We then start initializing our window
        super().__init__()

        self.setWindowTitle('Vulnerable environment generator.')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Main textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(col2, col2_row2)
        self.textbox.resize(700,400)
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText("Welcome to our vulnerable environement generator!\n"
                                  "This application uses docker containers to generate environments you can interact with, please make sure you have docker installed on your machine.")
        #self.textbox.setText("Welcome to our vulnerable environement generator!\n"
                             #"This application uses Docker Containers to generate environments you can interact with, please make sure you have docker installed on your machine.")
        self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Main entry
        #self.entry = QLineEdit(self)  
        #self.entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "#FFFFFF"')

        # Buttons


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())