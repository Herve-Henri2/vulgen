import sys

from application import *
from custom_images_window import *
import docker_utils as dutils

class ImagesWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None, containerMode=False):

        self.parent = parent
        self.containerMode = containerMode

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)


    def initUI(self, width, height):

        self.setWindowTitle('Images')
        self.setFixedSize(width, height)

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 300)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.ImageClicked)
        
        if not self.containerMode:
            # TextBox
            self.textbox = QPlainTextEdit(self)
            self.textbox.move(200, 330)
            self.textbox.resize(460, 100)
            self.textbox.setReadOnly(True)

            # Buttons            
            self.build_button = QPushButton('Build custom image', self)
            self.build_button.move(40, 330)
            self.build_button.resize(140, 20)
            self.build_button.clicked.connect(self.BuildCustomImage)
            
            self.remove_button = QPushButton('Remove', self)
            self.remove_button.move(40, 360)
            self.remove_button.resize(140, 20)
            self.remove_button.clicked.connect(self.RemoveImage)
        else:
            self.table_view.resize(620, 400)

            # Button
            self.create_button = QPushButton('Create container', self)
            self.create_button.move(50, 430)
            self.create_button.resize(120, 20)
            self.create_button.clicked.connect(self.CreateContainer)
            self.DisableButton(self.create_button)
        
        
        # Button
        self.refresh_button = QPushButton('R.', self)
        self.refresh_button.move(10, 20)
        self.refresh_button.resize(20, 20)
        self.refresh_button.clicked.connect(self.updateTable)           
        
        # Fill the table
        self.updateTable()

        # Styling and coloring
        self.ImplementTheme()
        if self.remove_button is not None:
            self.DisableButton(self.remove_button)
            

    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def ImageClicked(self):
        if not self.containerMode:
            self.EnableButton(self.remove_button)
        else:
            self.EnableButton(self.create_button)
    
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
            docker_client.images.remove(id)
            self.setText("Image successfully removed!")
            logger.info(f"Deleted the image {selection[1].text() + ':' + selection[2].text()}")
        except Exception as ex:
            self.setText(str(ex))
            logger.error(f"Error while attempting to remove the image {selection[1].text() + ':' + selection[2].text()}: {ex}")
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
            docker_client.containers.create(img, stdin_open=True, tty=True) #stdion_open and tty = True <=> docker create -it
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