import sys
import os
from application import *

class OptionsWindow(QDialog, BaseWindow):

    # region =====Initializing=====

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
        
        self.docker_desktop_entry = QLineEdit(docker_desktop, self)
        self.docker_desktop_entry.move(50, 40)
        self.docker_desktop_entry.resize(400, 20)
        if operating_system != "Windows":
            self.docker_desktop_entry.setEnabled(False)
            self.DisableButton(self.browse_button)
        
        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(370, 260)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.Save)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.move(50, 70)
        self.browse_button.resize(80, 20)
        self.browse_button.clicked.connect(self.FileDialog)


        # Theme Combobox + Label

        self.themes_label = QLabel('Theme', self)
        self.themes_label.move(50, 100)

        self.themes = QComboBox(self)
        self.themes.move(50, 120)

        # Mode Combobox + Label

        self.modes_label = QLabel('Mode', self)
        self.modes_label.move(50, 150)

        self.modes = QComboBox(self)
        self.modes.move(50, 170)

        # Shell opening upon scenario launch

        self.auto_attach_label = QLabel('Auto attach container to terminal', self)
        self.auto_attach_label.move(50, 200)

        self.auto_attach_checkbox = QCheckBox(self)
        self.auto_attach_checkbox.move(50, 220)

        # Restart label
        self.restart_label = QLabel('(Restart the app to apply the new parameters)', self)
        self.restart_label.move(100, 263)

        # Initializing
        self.Initialize()

        # Styling and coloring
        self.ImplementTheme()


    # endregion

    # region =====Graphical Methods=====
        
    # endregion

    # region =====General Methods=====

    def Initialize(self):
        if operating_system != "Windows":
            self.docker_desktop_entry.setEnabled(False)

        for theme in configuration['themes']:
            self.themes.addItem(theme['name'])
        self.themes.setCurrentText(configuration['themes'][configuration['current_theme_index']]['name'])

        for mode in configuration['modes']:
            self.modes.addItem(mode)
        self.modes.setCurrentText(configuration['modes'][configuration['current_mode_index']])

        if configuration['auto_attach'] is True:
            self.auto_attach_checkbox.setChecked(True)

    def FileDialog(self):
        '''
        Opens a file dialog to search for Docker Desktop.exe
        '''
        fname = QFileDialog.getOpenFileName(self, "Select the Docker Desktop.exe file", "", 'All Files (*Desktop.exe)')

        if fname:
            self.docker_desktop_entry.setText(fname[0])

    def Save(self):
        '''
        Writes the selected/entered parameters into the config.json file.
        '''
        allowed_to_close = True

        # We check that the entered docker path is correct
        if operating_system == "Windows" and (not os.path.exists(self.docker_desktop_entry.text()) or "Docker Desktop.exe" not in self.docker_desktop_entry.text()):
            messagebox = QMessageBox(self)
            messagebox.resize(200, 200)
            messagebox.setWindowTitle("Invalid Docker Desktop path")
            messagebox.setText('The Docker Desktop path is invalid! \nPlease select the correct path to "Docker Desktop.exe"\t')
            messagebox.setStyleSheet('background-color: white')
            messagebox.exec()
            allowed_to_close = False
        if allowed_to_close:
            if operating_system == "Windows":
                config.Save('docker_desktop', self.docker_desktop_entry.text())
            config.Save('current_theme_index', self.themes.currentIndex())
            config.Save('current_mode_index', self.modes.currentIndex())
            if self.auto_attach_checkbox.isChecked():
                config.Save('auto_attach', True)
            else:
                config.Save('auto_attach', False)
            self.close()

    #endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OptionsWindow()
    ex.show()
    sys.exit(app.exec())