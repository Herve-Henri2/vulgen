import sys

from application import *
import docker_utils as dutils
from scenarios import *


class ScenariosWindow(QDialog, BaseWindow):
    # region =====Initializing=====

    def __init__(self, parent=None):
        self.parent = parent
        self.scenarios : dict[str, Scenario] = scenarios_db['scenarios']
        self.current_scenario_images = dict[str, Image]()

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self,width, height):

        self.setWindowTitle('Scenarios')
        self.setFixedSize(width, height)

        # Default UI elements
        self.default_mode_ui = []
        
        # Side ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(200, 400)
        self.list_view.itemClicked.connect(self.showDetails)
        self.default_mode_ui.append(self.list_view)

        # Side TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(240, 20)
        self.textbox.resize(420, 400)
        self.textbox.setReadOnly(True)
        self.default_mode_ui.append(self.textbox)

        # Buttons
        self.launch_button = QPushButton('Launch Scenario', self)
        self.launch_button.move(540, 440)
        self.launch_button.resize(120, 20)
        self.launch_button.clicked.connect(self.LaunchScenario)
        self.default_mode_ui.append(self.launch_button)

        self.edit_button = QPushButton('Edit Scenario', self)
        self.edit_button.move(400, 440)
        self.edit_button.resize(120, 20)
        self.edit_button.clicked.connect(self.EditScenarioMode)
        self.default_mode_ui.append(self.edit_button)

        self.add_button = QPushButton('Add Scenario', self)
        self.add_button.move(260, 440)
        self.add_button.resize(120, 20)
        self.add_button.clicked.connect(self.AddScenarioMode)
        self.default_mode_ui.append(self.add_button)

        for scenario_name in self.scenarios:
            self.list_view.addItem(scenario_name)

        # Add & Edit mode UI elements
        self.edit_mode_ui = []

        # Buttons
        self.back_button = QPushButton('Back', self)
        self.back_button.move(20, 440)
        self.back_button.resize(80, 20)
        self.back_button.clicked.connect(self.DefaultMode)
        self.edit_mode_ui.append(self.back_button)

        self.save_button = QPushButton('Save', self)
        self.save_button.move(120, 440)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.SaveScenario)
        self.edit_mode_ui.append(self.save_button)

        self.add_image_button = QPushButton('Add', self)
        self.add_image_button.move(600, 290)
        self.add_image_button.clicked.connect(self.OpenImageAdd)
        self.edit_mode_ui.append(self.add_image_button)

        self.edit_image_button = QPushButton('Edit', self)
        self.edit_image_button.move(600, 320)
        self.edit_image_button.clicked.connect(self.OpenImageEdit)
        self.edit_mode_ui.append(self.edit_image_button)

        self.remove_image_button = QPushButton('Remove', self)
        self.remove_image_button.move(600, 350)
        self.remove_image_button.clicked.connect(self.RemoveImage)
        self.edit_mode_ui.append(self.remove_image_button)
        
        # Scenario Name
        self.scenario_name_label = QLabel('Scenario Name', self)
        self.scenario_name_label.move(20, 20)
        self.edit_mode_ui.append(self.scenario_name_label)

        self.scenario_name = QLineEdit(self)
        self.scenario_name.move(20, 40)
        self.scenario_name.resize(140, 20)
        self.edit_mode_ui.append(self.scenario_name)

        # Type
        self.type_label = QLabel('Type', self)
        self.type_label.move(180, 20)
        self.edit_mode_ui.append(self.type_label)

        self.type_entry = QLineEdit(self)
        self.type_entry.move(180, 40)
        self.type_entry.resize(140, 20)
        self.edit_mode_ui.append(self.type_entry)

        # CVE
        self.cve_label = QLabel('CVE', self)
        self.cve_label.move(340, 20)
        self.edit_mode_ui.append(self.cve_label)

        self.cve_entry = QLineEdit(self)
        self.cve_entry.move(340, 40)
        self.cve_entry.resize(140, 20)
        self.edit_mode_ui.append(self.cve_entry)
        
        # Difficulty
        self.diff_label = QLabel('Difficulty (/5)', self)
        self.diff_label.move(500, 20)
        self.edit_mode_ui.append(self.diff_label)

        self.diff_entry = QLineEdit(self)
        self.diff_entry.move(500, 40)
        self.diff_entry.resize(140, 20)
        self.edit_mode_ui.append(self.diff_entry)

        # Description
        self.scenario_desc_label = QLabel('Description', self)
        self.scenario_desc_label.move(20, 80)
        self.edit_mode_ui.append(self.scenario_desc_label)

        self.scenario_desc = QPlainTextEdit(self)
        self.scenario_desc.move(20, 100)
        self.scenario_desc.resize(300, 150)
        self.edit_mode_ui.append(self.scenario_desc)

        # Solution
        self.solution_label = QLabel('Solution', self)
        self.solution_label.move(340, 150)
        self.edit_mode_ui.append(self.solution_label)

        self.solution = QPlainTextEdit(self)
        self.solution.move(340, 170)
        self.solution.resize(300, 80)
        self.edit_mode_ui.append(self.solution)

        # Goal
        self.goal_label = QLabel('Goal', self)
        self.goal_label.move(20, 270)
        self.edit_mode_ui.append(self.goal_label)

        self.goal = QPlainTextEdit(self)
        self.goal.move(20, 290)
        self.goal.resize(300, 40)
        self.edit_mode_ui.append(self.goal)

        # Sources
        self.sources_label = QLabel('Sources', self)
        self.sources_label.move(20, 350)
        self.edit_mode_ui.append(self.sources_label)

        self.sources = QPlainTextEdit(self)
        self.sources.move(20, 370)
        self.sources.resize(300, 40)
        self.edit_mode_ui.append(self.sources)

        # Images
        self.images_label = QLabel('Images', self)
        self.images_label.move(340, 270)
        self.edit_mode_ui.append(self.images_label)

        self.images_list_view = QListWidget(self)
        self.images_list_view.move(340, 290)
        self.images_list_view.resize(250, 120)
        self.images_list_view.itemClicked.connect(self.AllowOpening)
        self.edit_mode_ui.append(self.images_list_view)

        self.HideUIElements(self.edit_mode_ui)

        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.edit_button, self.launch_button, self.edit_image_button, self.remove_image_button)

    # endregion

    # region =====Graphical Methods=====

    def showDetails(self):
        scenario_name = self.list_view.currentItem().text()
        scenario = self.scenarios[scenario_name]
        self.setText(scenario.description
                    +f"\n-----------------------------\nGoal: {scenario.goal}"
                    +f"\n-----------------------------\nType: {scenario.type}"
                    +f"\n-----------------------------\nCVE: {scenario.cve}")
        self.EnableButton(self.launch_button)
        self.EnableButton(self.edit_button)
    
    def AllowOpening(self):
        self.EnableButtons(self.edit_image_button, self.remove_image_button)

    def HideUIElements(self, ui_elements):
        for element in ui_elements:
            element.hide()

    def ShowUIElements(self, ui_elements):
        for element in ui_elements:
            element.show()

    def OpenImageAdd(self):
        window = EditImagesWindow(parent=self, addingMode=True)
        window.exec()

    def OpenImageEdit(self):
        selected_image_name = self.images_list_view.currentItem().text().replace('(main) ', '')
        selected_image = self.current_scenario_images[selected_image_name]
        window = EditImagesWindow(parent=self, image_to_edit=selected_image)
        window.exec()

    def RemoveImage(self):
        messagebox = QMessageBox(self)
        messagebox.setStyleSheet('background-color: blue')
        messagebox.question(self, 'Removing image', 'Are you sure you want to remove that image?\n(Note: This will not delete the image but only remove it from the scenario)')
        #messagebox.setText('This will not delete the container but only remove it from the scenario.')
        #TODO Remove container and update view

    # endregion

    # region =====Main Methods=====

    def LaunchScenario(self):
        scenario_name = self.list_view.currentItem().text()
        self.parent.LaunchScenario(scenario_name)
        self.close()

    def EditScenarioMode(self):
        '''
        Switches the window's UI to edit mode.
        '''
        # Setting up the UI
        self.HideUIElements(self.default_mode_ui)
        self.ShowUIElements(self.edit_mode_ui)

        selected_scenario_name = self.list_view.currentItem().text()
        scenario = self.scenarios[selected_scenario_name]
        self.scenario_name.setText(scenario.name)
        self.type_entry.setText(scenario.type)
        self.cve_entry.setText(scenario.cve)
        self.diff_entry.setText(str(scenario.difficulty))
        self.scenario_desc.setPlainText(scenario.description)
        self.solution.setPlainText(scenario.solution)
        self.goal.setPlainText(scenario.goal)
        for source in scenario.sources:
            self.sources.appendPlainText(source)
        for image in scenario.images.values():
            self.current_scenario_images[image.name] = image
            self.images_list_view.addItem(f"(main) {image.name}") if image.is_main is True else self.images_list_view.addItem(image.name)
                

    def AddScenarioMode(self):
        '''
        Switches the window's UI to add mode.
        '''
        # Setting up the UI
        self.HideUIElements(self.default_mode_ui)
        self.ShowUIElements(self.edit_mode_ui)

    def DefaultMode(self):
        '''
        Resets the window's UI back to default.
        '''
        #TODO add unsaved changed confirmation
        self.HideUIElements(self.edit_mode_ui)
        self.ShowUIElements(self.default_mode_ui)
        self.DisableButtons(self.edit_button, self.launch_button, self.edit_image_button, self.remove_image_button)
        self.current_scenario_images.clear()
        for element in self.edit_mode_ui:
            if isinstance(element, QLineEdit) or isinstance(element, QPlainTextEdit) or isinstance(element, QListWidget):
                element.clear()

    def SaveScenario(self):
        '''
        Saves the changes made to the scenario to the scenarios.json file.
        '''
        global scenarios_db
        
        def CheckValid():
            # TODO check if scenario name not already exists when adding
            import regex

            result = dict()
            result['valid_scenario'] = True
            result['message'] = ''
            
            # Name
            name = self.scenario_name.text()
            if len(name) == 0:
                result['valid_scenario'] = False
                result['message'] += f'Name cannot be empty!' + '\n'
            
            # CVE
            cve = self.cve_entry.text()
            if(len(cve) != 0):
                cve_expression = "^CVE-20[0-9]{2}-[0-9]{4,6}$"
                if regex.search(cve_expression, cve) is None:
                    result['valid_scenario'] = False
                    result['message'] += 'Your CVE is in the wrong format or does not exist.\nA CVE must be written in the following format: CVE-YYYY-NNNN' + '\n'

            # Difficulty
            min_difficulty = 1; max_difficulty = 5
            difficulty = self.diff_entry.text()
            if len(difficulty) != 0:
                if difficulty.isdigit():
                    difficulty = int(difficulty)
                    if difficulty < min_difficulty or difficulty > max_difficulty:
                        result['valid_scenario'] = False
                        result['message'] += 'The difficulty, if specified, must be an integer between 1 and 5!' + '\n'
                else:
                    result['valid_scenario'] = False
                    result['message'] += 'The difficulty, if specified, must be an integer between 1 and 5!' + '\n'
            
            # Images
            if self.images_list_view.count() == 0:
                result['valid_scenario'] = False
                result['message'] += 'You need at least one image in your scenario!' + '\n'
            
            return result
        
        is_valid = CheckValid()
        if is_valid['valid_scenario'] is False:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Invalid parameters!")
            messagebox.setText(is_valid['message'])
            messagebox.setStyleSheet('background-color: white; color: black')
            messagebox.exec()
        else:
            scenario_to_save = Scenario()
            scenario_to_save.name = self.scenario_name.text()
            scenario_to_save.description = self.scenario_desc.toPlainText()
            scenario_to_save.goal = self.goal.toPlainText()
            scenario_to_save.solution = self.solution.toPlainText()
            scenario_to_save.cve = self.cve_entry.text()
            scenario_to_save.difficulty = self.diff_entry.text()
            scenario_to_save.type = self.type_entry.text()
            scenario_to_save.sources = [str(source) for source in self.sources.toPlainText().split('\n') if len(source) > 0]
            scenario_to_save.images = self.current_scenario_images
            
            scenarios.Save(scenario_to_save)
            scenarios_db = scenarios.Load()
            self.scenarios = scenarios_db['scenarios']
            self.list_view.clear()
            for scenario_name in self.scenarios:
                self.list_view.addItem(scenario_name)
            self.DefaultMode()
        
        

    # endregion

class EditImagesWindow(QDialog, BaseWindow):
    
    # region =====Initializing=====

    def __init__(self, parent = None, addingMode = False, image_to_edit : Image = None):

        self.parent = parent
        self.addingMode = addingMode
        if self.addingMode is False:
            self.image_to_edit = image_to_edit

        # Defining our layout variables
        width = 600
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):
        self.setWindowTitle('Add | Edit scenario image')
        self.setFixedSize(width, height)

        # Image selection
        self.image_label = QLabel('From existing image', self)
        self.image_label.move(20, 20)

        self.images = QComboBox(self)
        self.images.move(20, 40)
        self.images.resize(300, 20)

        # Dockerfile entry
        self.dockerfile_label = QLabel('From Dockerfile', self)
        self.dockerfile_label.move(20, 70)

        self.dockerfile_entry = QLineEdit(self)
        self.dockerfile_entry.move(20, 90)
        self.dockerfile_entry.resize(300, 20)
        self.dockerfile_entry.setPlaceholderText('Put the dockerfile path here')

        # Main image or not?
        self.is_main_label = QLabel('Main Image?', self)
        self.is_main_label.move(350, 20)

        self.is_main = QComboBox(self)
        self.is_main.move(350, 40)
        self.is_main.addItems(['Yes', 'No'])

        # Container port
        self.container_port_label = QLabel('Container port', self)
        self.container_port_label.move(350, 70)

        self.container_port = QLineEdit(self)
        self.container_port.move(350, 90)
        self.container_port.resize(100, 20)

        # Host port
        self.host_port_label = QLabel('Host port', self)
        self.host_port_label.move(460, 70)

        self.host_port = QLineEdit(self)
        self.host_port.move(460, 90)
        self.host_port.resize(100, 20)

        # Operating System
        self.image_os_label = QLabel('Operating system', self)
        self.image_os_label.move(20, 150)

        self.image_os = QLineEdit(self)
        self.image_os.move(20, 170)
        self.image_os.resize(150, 20)

        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(20, 440)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.SaveImage)

        self.browse_button = QPushButton('browse', self) #Browse for dockerfile
        self.browse_button.move(20, 120)
        self.browse_button.resize(80, 20)
        self.browse_button.clicked.connect(self.FileDialog)

        self.ImplementTheme(self.dockerfile_entry)
        self.dockerfile_entry.setStyleSheet(f'background-color: {theme["main_window_textbox_color"]}; color: {theme["text_color"]};'
                                            f'font-family: {theme["text_font"]}; font-style: italic; border: 1px solid "{theme["border_color"]}"')

        self.FillFields()

    # endregion

    # region =====Graphical Methods=====

    # endregion

    # region =====Main Methods=====

    def FileDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Select the DockerFile", "", 'All Files (Dockerfile)')

        if fname:
            self.dockerfile_entry.setText(fname[0])

    def FillFields(self):        
        # Adding the existing images
        if self.addingMode is True:
            self.images.addItem('None')
        else:
            self.images.addItem(self.image_to_edit.name)

        for image in self.docker_client.images.list():
            if self.addingMode is False and self.image_to_edit.name in image.tags[0].split(':')[0]:
                continue
            self.images.addItem(image.tags[0])

        # Filling the other fields (or not)
        if self.addingMode is False:
            if self.image_to_edit.is_main is True:
                self.is_main.setCurrentText('Yes')
            else:
                self.is_main.setCurrentText('No')
            self.image_os.setText(self.image_to_edit.os)
            for key, value in self.image_to_edit.ports.items():
                self.container_port.setText(key)
                self.host_port.setText(value)

    def SaveImage(self):
        
        def CheckValid():
            result = {}
            result['is_valid'] = True
            result['message'] = ""
            
            # Name & Dockerfile
            name = self.images.currentText()
            dockerfile = self.dockerfile_entry.text()
            if name == "None" and len(dockerfile) == 0:
                result['is_valid'] = False
                result['message'] += 'You need to select either an image or a dockerfile!' + '\n'
            
            # Ports
            ports = (self.container_port.text(), self.host_port.text())
            if len(ports[0]) != 0 or len(ports[1]) != 0:
                if not ports[0].isdigit() or not ports[1].isdigit():
                    result['is_valid'] = False
                    result['message'] += 'If specified, the ports number must be positive integers!' + '\n'

            return result

        is_valid = CheckValid()
        if is_valid['is_valid'] is False:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Invalid parameters!")
            messagebox.setText(is_valid['message'])
            messagebox.setStyleSheet('background-color: white; color: black')
            messagebox.exec()
        else:
            image_to_save = Image()
            image_to_save.name = self.images.currentText()
            image_to_save.dockerfile = self.dockerfile_entry.text()
            image_to_save.is_main = True if self.is_main.currentText() == "Yes" else False
            if len(self.container_port.text()) != 0 and len(self.host_port.text()) != 0:
                image_to_save.ports = {self.container_port.text() : self.host_port.text()}
            image_to_save.os = self.image_os.text()
            
            self.parent.current_scenario_images[image_to_save.name] = image_to_save
            if self.addingMode is True:
                self.parent.images_list_view.addItem(f"(main) {image_to_save.name}") if image_to_save.is_main else self.parent.images_list_view.addItem(image_to_save.name)
            else:
                for item in self.parent.images_list_view.items():
                    if item.text().replace("(main) ", "") == image_to_save.name:
                        item.setText(image_to_save.name)                

            self.close()

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())