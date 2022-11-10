from PyQt6.QtWidgets import *
import config
import sys
import docker
import docker_utils as dutils
from images_window import *

configuration = config.Load()

class ContainersWindow(QDialog):

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

        self.setWindowTitle('Containers')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 400)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.ContainerClicked)
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
        
        self.start_button = QPushButton('Start container', self)
        self.start_button.move(50, 425)
        self.start_button.resize(120, 20)
        self.start_button.clicked.connect(self.StartContainer)
        self.start_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.start_button)
        
        self.create_button = QPushButton('Create container', self)
        self.create_button.move(50, 450)
        self.create_button.resize(120, 20)
        self.create_button.clicked.connect(self.CreateContainer)
        self.create_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.move(50, 475)
        self.remove_button.resize(120, 20)
        self.remove_button.clicked.connect(self.RemoveContainer)
        self.remove_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.remove_button)
        
        # Fill the table
        self.updateTable()
        
            

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def ContainerClicked(self):
        self.EnableButton(self.start_button)
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
        cont_dict = dutils.GetContainers()
        
        self.table_view.setColumnCount(len(cont_dict.keys()))
        self.table_view.setRowCount(len(cont_dict['id']))
        self.table_view.setHorizontalHeaderLabels(cont_dict.keys())    
        for c,key in enumerate(cont_dict.keys()):
            for r,val in enumerate(cont_dict[key]):
                newitem = QTableWidgetItem(val)
                self.table_view.setItem(r, c, newitem)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()


    # endregion

    # region =====Main Methods=====
    
    def StartContainer(self):
        selection = self.table_view.selectedItems()
        id = selection[0].text()
        command = f"docker start -i {id}"
        misc.open_terminal(command =command)

    def RemoveContainer(self):
        selection = self.table_view.selectedItems()
        id = selection[0].text()
        try:
            self.docker_client.containers.get(id).remove()
            self.setText("Container successfully removed !")
        except Exception as ex:
            self.setText(str(ex))
        self.updateTable()
    
    def CreateContainer(self):
        self.images_window = ImagesWindow(parent=self, containerMode=True)
        self.images_window.exec()

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ContainersWindow()
    ex.show()
    sys.exit(app.exec())