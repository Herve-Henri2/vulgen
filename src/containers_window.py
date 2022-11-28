from PyQt6.QtWidgets import *
import sys
import misc
import docker_utils as dutils
from images_window import *
from application import *

class ContainersWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):

        self.setWindowTitle('Containers')
        self.setFixedSize(width, height)

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 300)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.ContainerClicked)

        # TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(180, 330)
        self.textbox.resize(480, 110)
        self.textbox.setReadOnly(True)

        # Buttons
        self.refresh_button = QPushButton('R.', self)
        self.refresh_button.move(10, 20)
        self.refresh_button.resize(20, 20)
        self.refresh_button.clicked.connect(self.updateTable)
        
        self.start_button = QPushButton('Start container', self)
        self.start_button.move(50, 330)
        self.start_button.resize(120, 20)
        self.start_button.clicked.connect(self.StartContainer)

        self.stop_button = QPushButton('Stop container', self)
        self.stop_button.move(50, 360)
        self.stop_button.resize(120, 20)
        self.stop_button.clicked.connect(self.StopContainer)
        
        self.create_button = QPushButton('Create container', self)
        self.create_button.move(50, 390)
        self.create_button.resize(120, 20)
        self.create_button.clicked.connect(self.CreateContainer)
        
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.move(50, 420)
        self.remove_button.resize(120, 20)
        self.remove_button.clicked.connect(self.RemoveContainer)
        
        self.attach_button = QPushButton('Attach to terminal', self)
        self.attach_button.move(300, 450)
        self.attach_button.resize(240, 20)
        self.attach_button.clicked.connect(self.AttachContainer)
        
        # Fill the table
        self.updateTable()
        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.start_button, self.stop_button, self.remove_button, self.attach_button)
        
    # endregion

    # region =====Graphical Methods=====

    def ContainerClicked(self):
        selection = self.table_view.selectedItems()
        status = selection[3].text()
        if status == 'running':
            self.EnableButtons(self.stop_button, self.attach_button)
        else:
            self.EnableButton(self.start_button)
        self.EnableButton(self.remove_button)
        
    def updateTable(self):
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
        '''
        Starts the selected container.
        '''
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        self.docker_client.containers.get(id).start()
        self.updateTable()
        selection = self.table_view.selectedItems()
        if status := selection[3].text() == 'running':
            self.DisableButton(self.start_button)
            self.EnableButtons(self.stop_button, self.attach_button)
            logger.info(f'Started the container {selection[1].text()}')
            self.setText(f'Started the container {selection[1].text()}')

    def StopContainer(self):
        '''
        Stops the selected container.
        '''
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        self.docker_client.containers.get(id).stop()
        self.updateTable()
        selection = self.table_view.selectedItems()
        if status := selection[3].text() == 'exited':
            self.DisableButtons(self.stop_button, self.attach_button)
            self.EnableButton(self.start_button)
            logger.info(f'Stopped the container {selection[1].text()}')
            self.setText(f'Stopped the container {selection[1].text()}')


    def RemoveContainer(self):
        '''
        Deletes the selected container.
        '''
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        try:
            name = self.docker_client.containers.get(id).name
            self.docker_client.containers.get(id).remove()
            self.setText("Container successfully removed!")
            logger.info(f'Removed the container {name}')
        except Exception as ex:
            self.setText(str(ex))
            logger.info(ex)
        self.updateTable()
    
    
    def AttachContainer(self):
        '''
        Attach the container to a new terminal.
        '''
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        try:
            container = self.docker_client.containers.get(id)
            self.setText(f'Opening up a terminal for the {container.name} container.')
            logger.info(f'Opening up a terminal for the {container.name} container.')
            command = f"docker logs {id};docker attach {id}"
            misc.open_terminal(operating_system, command)
        except Exception as ex:
            self.setText(str(ex))
            logger.info(ex)
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
