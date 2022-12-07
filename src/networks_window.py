from PyQt6.QtWidgets import *
import sys
import docker_utils as dutils
from application import *

class NetworksWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):

        self.setWindowTitle('Networks')
        self.setFixedSize(width, height)

        # TableView
        self.table_view = QTableWidget(self)
        self.table_view.move(40, 20)
        self.table_view.resize(620, 300)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.itemClicked.connect(self.NetworkClicked)

        # TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(180, 330)
        self.textbox.resize(480, 110)
        self.textbox.setReadOnly(True)

        # Buttons
        self.refresh_button = QPushButton('', self)
        self.refresh_button.setIcon(QtGui.QIcon(src_folder_path + f"{sep}..{sep}images{sep}refresh.png"))
        self.refresh_button.setIconSize(QSize(24,24))
        self.refresh_button.move(10, 20)
        self.refresh_button.resize(24, 24)
        self.refresh_button.clicked.connect(self.updateTable)
        
        self.create_button = QPushButton('Create network', self)
        self.create_button.move(50, 330)
        self.create_button.resize(120, 20)
        self.create_button.clicked.connect(self.CreateNetwork)
        
        self.connect_button = QPushButton('Connect to container', self)
        self.connect_button.move(50, 360)
        self.connect_button.resize(120, 20)
        self.connect_button.clicked.connect(self.ConnectContainer)

        self.remove_button = QPushButton('Remove network', self)
        self.remove_button.move(50, 390)
        self.remove_button.resize(120, 20)
        self.remove_button.clicked.connect(self.RemoveNetwork)
        
        # Fill the table
        self.updateTable()
        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.connect_button, self.remove_button)
        
    # endregion

    # region =====Graphical Methods=====

    def NetworkClicked(self):
        self.EnableButtons(self.connect_button, self.remove_button)
        
    def updateTable(self):
        network_dict = dutils.GetNetworks()
        
        self.table_view.setColumnCount(len(network_dict.keys()))
        self.table_view.setRowCount(len(network_dict['id']))
        self.table_view.setHorizontalHeaderLabels(network_dict.keys())    
        for c,key in enumerate(network_dict.keys()):
            for r,val in enumerate(network_dict[key]):
                newitem = QTableWidgetItem(val)
                self.table_view.setItem(r, c, newitem)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()


    # endregion

    # region =====Main Methods=====

    def CreateNetwork(self):
        # For now you can only configure the network name (maybe that is all we need)
        name, ok = QInputDialog.getText(self, 'Network name input', "Give a name to the new network:")
        if ok:
            self.docker_client.networks.create(name, driver="bridge")
            self.updateTable()
    
    def ConnectContainer(self):
        '''
        Connects a container to the selected network
        '''
        containers = self.docker_client.containers.list(all=True)
        if len(containers) != 0:
            containers = [f"{cont.short_id}-{cont.image.tags[0]}" for cont in containers]
            container, ok = QInputDialog.getItem(self, "Container input", "List of containers:", containers, 0, False)	
            if ok and container:            
                try:
                    selection = self.table_view.selectedItems()
                    id = selection[0].text()
                    network = self.docker_client.networks.get(id)
                    container_id = container.split('-')[0]
                    network.connect(container_id)
                    self.setText("Container successfully connected!")
                    logger.info(f'Container {container_id} connected to the network {network.name}')
                except Exception as ex:
                    self.setText(str(ex))
                    logger.info(ex)
                self.updateTable()
        else:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Error")
            messagebox.setText("No containers available!")
            messagebox.exec()

    def RemoveNetwork(self):
        '''
        Removes the selected network.
        '''
        selection = self.table_view.selectedItems()
        if selection is None or len(selection) == 0:
            return
        id = selection[0].text()
        try:
            self.docker_client.networks.get(id).remove()
            name = selection[1].text()
            self.setText("Network successfully removed!")
            logger.info(f'Removed the network {name}')
        except Exception as ex:
            self.setText(str(ex))
            logger.info(ex)
        self.updateTable()

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NetworksWindow()
    ex.show()
    sys.exit(app.exec())