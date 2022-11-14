from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import config
import sys
import os
from base_window import *

configuration = config.Load()
operating_system = configuration['operating_system']

class OptionsWindow(QDialog, BaseWindow):

    # region =====Initializing=====
    docker_client_path = configuration['docker_desktop']

    def __init__(self, parent=None):

        self.parent = parent

        # Defining our layout variables
        width = 500
        height = 300

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):

        self.setWindowTitle('Options')
        self.setFixedSize(width, height)

        # Docker Desktop file path

        self.docker_path_label = QLabel('Docker Desktop path (Windows Only)', self)
        self.docker_path_label.move(50, 20)
        self.docker_path_label.resize(400, 20)
        
        self.docker_desktop_entry = QLineEdit(self.docker_client_path, self)
        self.docker_desktop_entry.move(50, 40)
        self.docker_desktop_entry.resize(400, 20)
        if operating_system != "Windows":
            self.docker_desktop_entry.setEnabled(False)
        

        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(370, 260)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.Save)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.move(50, 70)
        self.browse_button.resize(80, 20)
        self.browse_button.clicked.connect(self.FileDialog)
        if operating_system != "Windows":
            self.docker_desktop_entry.setEnabled(False)

        # Theme Combobox + Label

        self.themes_label = QLabel('Theme', self)
        self.themes_label.move(50, 100)
        self.themes_label.resize(80, 20)

        self.themes = QComboBox(self)
        self.themes.move(50, 120)
        for theme in configuration['themes']:
            self.themes.addItem(theme['name'])
        self.themes.setCurrentText(configuration['themes'][configuration['current_theme_index']]['name'])
        # self.themes.activated.connect(self.setTheme)

        self.ImplementTheme()


    # endregion

    # region =====Graphical Methods=====

    def setTheme(self, index):
        config.Save('current_theme_index', index)
        
    # endregion

    # region =====General Methods=====

    def FileDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Select the Docker Desktop.exe file", "", 'All Files (*Desktop.exe)')

        if fname:
            self.docker_desktop_entry.setText(fname[0])

    def Save(self):

        allowed_to_close = True

        # We check that the docker path entered is correct
        if not os.path.exists(self.docker_desktop_entry.text()) or "Docker Desktop.exe" not in self.docker_desktop_entry.text():
            messagebox = QMessageBox(self)
            messagebox.resize(200, 200)
            messagebox.setWindowTitle("Invalid Docker Desktop path")
            messagebox.setText('The Docker Desktop path is invalid! \nPlease select the correct path to "Docker Desktop.exe"\t')
            messagebox.setStyleSheet('background-color: white')
            messagebox.exec()
            allowed_to_close = False
        if allowed_to_close:
            config.Save('docker_desktop', self.docker_desktop_entry.text())
            config.Save('current_theme_index', self.themes.currentIndex())
            self.close()

    #endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OptionsWindow()
    ex.show()
    sys.exit(app.exec())