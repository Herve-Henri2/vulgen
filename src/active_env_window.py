import sys

from application import *
import misc


class ActiveEnvWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent=parent

        # Defining our layout variables
        width = 500
        height = 300

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):
        self.setWindowTitle('Environment Containers')
        self.setFixedSize(width, height)

        # Main ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(400, 200)
        self.list_view.itemClicked.connect(self.AllowShell)

        # Buttons
        self.open_shell_button = QPushButton('Open Shell', self)
        self.open_shell_button.move(40, 240)
        self.open_shell_button.resize(120, 20)
        self.open_shell_button.clicked.connect(self.AttachContainer)

        if self.parent is not None:
            self.containers = self.parent.GetRunningScenarioContainers()
            for container in self.containers:
                self.list_view.addItem(f'{container.name} - {container.ports}')

        # Styling and coloring
        self.ImplementTheme()
        self.DisableButton(self.open_shell_button)

    # endregion

    # region =====Graphical Methods=====

    def AllowShell(self):
        self.EnableButton(self.open_shell_button)

    def AttachContainer(self):        
        selection = self.list_view.currentItem().text().split('|')[0][:-1]
        if selection is None or len(selection) == 0:
            return
        try:
            container = self.docker_client.containers.get(selection)
            logger.info(f'Opening up a terminal for the {selection} container.')
            command = f"docker logs {container.short_id};docker attach {container.short_id}"
            misc.open_terminal(operating_system, command)
        except Exception as ex:
            logger.info(ex)

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ActiveEnvWindow()
    ex.show()
    sys.exit(app.exec())