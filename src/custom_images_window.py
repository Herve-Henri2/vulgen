from PyQt6.QtWidgets import *
import config
import sys
import os
import docker
import misc
import docker_utils as dutils

configuration = config.Load()

class CustomImagesWindow(QDialog):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent
        self.docker_client = docker.from_env()

        # We define a few graphical variables from the configuration

        background_color = configuration['child_window_background_color']
        textbox_color = configuration['main_window_textbox_color']
        buttons_color = configuration['buttons_color']
        text_color = configuration['text_color']
        text_font = configuration['text_font']
        text_size = configuration['text_size']

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size)


    def initUI(self, background_color, textbox_color, width, height, buttons_color, text_color, text_font, text_size):

        self.setWindowTitle('Custom Images')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(620, 400)
        self.list_view.itemClicked.connect(self.ImageClicked)
        self.list_view.itemDoubleClicked.connect(self.BuildImage)
        self.list_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Buttons
        self.build_button = QPushButton('Build Image', self)
        self.build_button.move(290, 450)
        self.build_button.resize(120, 20)
        self.build_button.clicked.connect(self.BuildImage)
        self.build_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.build_button)
        
        # Fill the table
        self.updateList()
            

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def ImageClicked(self):
        self.EnableButton(self.build_button)

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
    
    def updateList(self):        
        dutils.docker_client = self.docker_client
        img_list = dutils.GetCustomImages()
        
        self.list_view.addItems(img_list)


    # endregion

    # region =====Main Methods=====

    def BuildImage(self):
        selection = self.list_view.currentItem().text()
        path = os.path.realpath(os.path.dirname(__file__)) + "/../docker_images"  # src folder absolute path + path to docker_images from src folder
        command = f"cd {path};{selection}/create_img.sh"
        misc.open_terminal(command = command)
        self.close()
        
            

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CustomImagesWindow()
    ex.show()
    sys.exit(app.exec())