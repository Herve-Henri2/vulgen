from PyQt6.QtWidgets import *
import config
import sys
import docker
import docker_utils as dutils
from custom_images_window import *

configuration = config.Load()

class ImagesWindow(QDialog):

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

        self.setWindowTitle('Images')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 400)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.ImageClicked)
        self.table_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")
        
        # TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(180, 430)
        self.textbox.resize(480, 60)
        self.textbox.setReadOnly(True)
        self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '#FFFFFF';")

        # Buttons
        self.refresh_button = QPushButton('R.', self)
        self.refresh_button.move(10, 20)
        self.refresh_button.resize(20, 20)
        self.refresh_button.clicked.connect(self.updateTable)
        self.refresh_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        
        self.build_button = QPushButton('Build custom image', self)
        self.build_button.move(50, 430)
        self.build_button.resize(120, 20)
        self.build_button.clicked.connect(self.BuildCustomImage)
        self.build_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.move(50, 460)
        self.remove_button.resize(120, 20)
        self.remove_button.clicked.connect(self.RemoveImage)
        self.remove_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.remove_button)
        
        # Fill the table
        self.updateTable()
            

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def ImageClicked(self):
        self.EnableButton(self.remove_button)

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
    
    def updateTable(self):        
        dutils.docker_client = self.docker_client
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
        try:
            id = selection[0].text()
            self.docker_client.images.remove(id)
            self.setText("Image successfully removed !")
        except Exception as ex:
            self.setText(str(ex))
        self.updateTable()
    
    def BuildCustomImage(self):
        self.custom_images_window = CustomImagesWindow(parent=self)
        self.custom_images_window.exec()
            

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImagesWindow()
    ex.show()
    sys.exit(app.exec())