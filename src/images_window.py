from PyQt6.QtWidgets import *
import config
import logging
import sys
import docker
import docker_utils as dutils
from custom_images_window import *

configuration = config.Load()
logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()

class ImagesWindow(QDialog):

    # region =====Initializing=====

    def __init__(self, parent=None, containerMode=False):

        self.parent = parent
        self.containerMode = containerMode
        self.docker_client = docker.from_env()

        # We define a few graphical variables from the configuration
        self.theme = config.GetTheme(configuration)
        background_color = self.theme['child_window_background_color']
        textbox_color = self.theme['main_window_textbox_color']
        buttons_color = self.theme['buttons_color']
        border_color = self.theme['border_color']
        text_color = self.theme['text_color']
        text_font = self.theme['text_font']
        text_size = self.theme['text_size']

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, border_color, text_color, text_font, text_size)


    def initUI(self, background_color, textbox_color, width, height, buttons_color, border_color, text_color, text_font, text_size):

        self.setWindowTitle('Images')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 300)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.ImageClicked)
        self.table_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")
        self.table_view.horizontalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")
        self.table_view.verticalHeader().setStyleSheet("::section{Background-color:" + str(textbox_color) + "}")
        
        if not self.containerMode:
            # TextBox
            self.textbox = QPlainTextEdit(self)
            self.textbox.move(200, 330)
            self.textbox.resize(460, 100)
            self.textbox.setReadOnly(True)
            self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")

            # Buttons            
            self.build_button = QPushButton('Build custom image', self)
            self.build_button.move(40, 330)
            self.build_button.resize(140, 20)
            self.build_button.clicked.connect(self.BuildCustomImage)
            self.build_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
            
            self.remove_button = QPushButton('Remove', self)
            self.remove_button.move(50, 360)
            self.remove_button.resize(120, 20)
            self.remove_button.clicked.connect(self.RemoveImage)
            self.remove_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
            self.DisableButton(self.remove_button)
        else:
            self.table_view.resize(620, 400)

            # Button
            self.create_button = QPushButton('Create container', self)
            self.create_button.move(50, 430)
            self.create_button.resize(120, 20)
            self.create_button.clicked.connect(self.CreateContainer)
            self.create_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
            self.DisableButton(self.create_button)
        
        
        # Button
        self.refresh_button = QPushButton('R.', self)
        self.refresh_button.move(10, 20)
        self.refresh_button.resize(20, 20)
        self.refresh_button.clicked.connect(self.updateTable)
        self.refresh_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')            
        
        # Fill the table
        self.updateTable()
            

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def ImageClicked(self):
        if not self.containerMode:
            self.EnableButton(self.remove_button)
        else:
            self.EnableButton(self.create_button)

    def DisableButton(self, button : QPushButton):
        buttons_color = self.theme['disabled_buttons_color']
        text_color = self.theme['disabled_text_color']
        text_font = self.theme['text_font']

        button.setEnabled(False)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font};')

    def EnableButton(self, button : QPushButton):
        buttons_color = self.theme['buttons_color']
        text_color = self.theme['text_color']
        text_font = self.theme['text_font']

        button.setEnabled(True)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
    
    def updateTable(self):        
        img_dict = dutils.GetImages()
        
        self.table_view.setColumnCount(len(img_dict.keys()))
        self.table_view.setRowCount(len(img_dict['id']))
        self.table_view.setHorizontalHeaderLabels(img_dict.keys())        
        for c,key in enumerate(img_dict.keys()):
            for r,val in enumerate(img_dict[key]):
                newitem = QTableWidgetItem(val)
                self.table_view.setItem(r, c, newitem)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()


    # endregion

    # region =====Main Methods=====

    def RemoveImage(self):
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        try:
            self.docker_client.images.remove(id)
            self.setText("Image successfully removed!")
            logger.info(f"Deleted the image {selection[1].text() + ':' + selection[2].text()}")
        except Exception as ex:
            self.setText(str(ex))
        self.updateTable()
    
    def BuildCustomImage(self):
        self.custom_images_window = CustomImagesWindow(parent=self)
        self.custom_images_window.exec()
    
    def CreateContainer(self):
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        img = selection[1].text() + ':' + selection[2].text()
        try:
            self.docker_client.containers.create(img, stdin_open=True, tty=True) #stdion_open and tty = True <=> docker create -it
            logger.info(f"Created a container for {img}")    
            self.parent.setText("Container successfully created!")
            self.parent.updateTable()
            self.close()
        except Exception as ex:
            self.parent.setText(str(ex))
            

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImagesWindow()
    ex.show()
    sys.exit(app.exec())