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
        self.open_shell_button.clicked.connect(self.OpenShell)

        self.logs_button = QPushButton('Attach to terminal', self)
        self.logs_button.move(180, 240)
        self.logs_button.resize(80, 20)
        self.logs_button.clicked.connect(self.AttachToTerminal)

        if self.parent is not None:
            self.containers = self.parent.GetRunningScenarioContainers()
            for container in self.containers:
                self.list_view.addItem(f'{container.name} | {container.ports}')

        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.open_shell_button, self.logs_button)

    # endregion

    # region =====Graphical Methods=====

    def AllowShell(self):
        self.EnableButtons(self.open_shell_button, self.logs_button)

    def OpenShell(self):
        selection = self.list_view.currentItem().text().split('|')[0][:-1]
        print(selection)
        if selection is None or len(selection) == 0:
            return
        try:
            container = self.docker_client.containers.get(selection)
            logger.info(f'Starting a terminal process for the {selection} container.')
            command = f"docker exec -it {container.short_id} /bin/sh"
            misc.open_terminal(operating_system, command)
        except Exception as ex:
            logger.info(ex)

    def AttachToTerminal(self):        
        selection = self.list_view.currentItem().text().split('|')[0][:-1]
        print(selection)
        if selection is None or len(selection) == 0:
            return
        try:
            container = self.docker_client.containers.get(selection)
            logger.info(f'Attaching the {selection} container to a new terminal.')
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