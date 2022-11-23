import sys

from application import *
import docker_utils as dutils
import scenarios


class ScenariosWindow(QDialog, BaseWindow):

    scenarios = scenarios_db['scenarios']

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent
        self.scen_to_save = scenarios.Scenario()

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self,width, height):

        self.setWindowTitle('Scenarios')
        self.setFixedSize(width, height)

        # Side ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(200, 400)
        self.list_view.itemClicked.connect(self.showDetails)

        # Side TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(240, 20)
        self.textbox.resize(420, 400)
        self.textbox.setReadOnly(True)

        # Buttons
        self.launch_button = QPushButton('Launch Scenario', self)
        self.launch_button.move(540, 440)
        self.launch_button.resize(120, 20)
        self.launch_button.clicked.connect(self.LaunchScenario)

        self.edit_button = QPushButton('Edit Scenario', self)
        self.edit_button.move(400, 440)
        self.edit_button.resize(120, 20)
        self.edit_button.clicked.connect(self.EditScenarioMode)

        self.add_button = QPushButton('Add Scenario', self)
        self.add_button.move(260, 440)
        self.add_button.resize(120, 20)
        self.add_button.clicked.connect(self.AddScenarioMode)

        for scenario in self.scenarios:
            self.list_view.addItem(scenario['name'])

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

        # Instructions
        self.instructions_label = QLabel('Instructions', self)
        self.instructions_label.move(340, 80)
        self.edit_mode_ui.append(self.instructions_label)

        self.instructions = QPlainTextEdit(self)
        self.instructions.move(340, 100)
        self.instructions.resize(300, 40)
        self.edit_mode_ui.append(self.instructions)

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

        self.HideEditUI()

        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.edit_button, self.launch_button, self.edit_image_button, self.remove_image_button)

    # endregion

    # region =====Graphical Methods=====

    def showDetails(self):
        for scenario in self.scenarios:
            if scenario['name'] == self.list_view.currentItem().text():
                self.setText(scenario['description']
                            +f"\n-----------------------------\nGoal: {scenario['goal']}"
                            +f"\n-----------------------------\nType: {scenario['type']}"
                            +f"\n-----------------------------\nCVE: {scenario['CVE']}")
        self.EnableButton(self.launch_button)
        self.EnableButton(self.edit_button)
    
    def AllowOpening(self):
        self.EnableButtons(self.edit_image_button, self.remove_image_button)

    def HideEditUI(self):
        for element in self.edit_mode_ui:
            element.hide()

    def ShowEditUI(self):
        for element in self.edit_mode_ui:
            element.show()

    def OpenImageAdd(self):
        window = EditImagesWindow(parent=self)
        window.exec()

    def OpenImageEdit(self):
        selected_image = self.images_list_view.currentItem().text().replace('(main) ', '')
        window = EditImagesWindow(parent=self, image=selected_image)
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
        scenario = self.list_view.currentItem().text()
        self.parent.LaunchScenario(scenario)
        self.close()

    def EditScenarioMode(self):
        '''
        Switches the window's UI to edit mode.
        '''
        # Setting up the UI
        self.launch_button.hide()
        self.edit_button.hide()
        self.add_button.hide()
        self.textbox.hide()
        self.list_view.hide()
        self.ShowEditUI()

        selected_scenario = self.list_view.currentItem().text()
        scenario = scenarios.Get(scenarios_db, selected_scenario)
        self.scen_to_save = scenario
        self.scenario_name.setText(scenario.name)
        self.type_entry.setText(scenario.type)
        self.cve_entry.setText(scenario.cve)
        self.diff_entry.setText(str(scenario.difficulty))
        self.scenario_desc.setPlainText(scenario.description)
        self.instructions.setPlainText(scenario.instructions)
        self.solution.setPlainText(scenario.solution)
        self.goal.setPlainText(scenario.goal)
        for source in scenario.sources:
            self.sources.appendPlainText(source)
        for image in scenario.images:
            if image['is_main'] is True:
                self.images_list_view.addItem(f"(main) {image['name']}")
            else:
                self.images_list_view.addItem(image['name'])

    def AddScenarioMode(self):
        '''
        Switches the window's UI to add mode.
        '''
        # Setting up the UI
        self.HideElements(self.launch_button, self.edit_button, self.add_button,
        self.textbox, self.list_view)
        self.ShowEditUI()

    def DefaultMode(self):
        '''
        Resets the window's UI back to default.
        '''
        #TODO add unsaved changed confirmation
        self.scen_to_save = None
        self.HideEditUI()
        self.ShowElements(self.launch_button, self.edit_button, self.add_button,
        self.textbox, self.list_view)
        self.DisableButtons(self.edit_button, self.launch_button, self.edit_image_button, self.remove_image_button)
        for element in self.edit_mode_ui:
            if isinstance(element, QLineEdit) or isinstance(element, QPlainTextEdit) or isinstance(element, QListWidget):
                element.clear()

    def SaveScenario(self):
        '''
        Saves the changes made to the scenario to the scenarios.json file.
        '''
        #TODO Check all the inputs!
        # if self.scen_to_save is None (for adding a new scenario)...

        global scenarios_db

        def CheckValid(scenario : scenarios.Scenario):
            import regex

            result = {}
            result['valid_scenario'] = True
            result['message'] = ''

            # A few variables we will use to do our checks
            none_not_allowed = ['name', 'description', 'goal', 'instructions', 'images', 'CVE', 'difficulty','type']
            min_difficulty = 1; max_difficulty = 5

            # Checking that some attributes are not none
            for attribute in scenario.__dict__:
                attribute_name = attribute
                attribute = getattr(scenario, attribute)
                if attribute_name in none_not_allowed:
                    if attribute is None or attribute == "":
                        result['valid_scenario'] = False
                        result['message'] = f'{attribute_name} cannot be empty!'
            # Checking valid difficulty
            try:
                scenario.difficulty = int(scenario.difficulty)
                if scenario.difficulty < min_difficulty or scenario.difficulty > max_difficulty:
                    result['valid_scenario'] = False
                    result['message'] = 'The difficulty must an integer between 1 and 5!'
            except ValueError:
                result['valid_scenario'] = False
                result['message'] = 'The difficulty must an integer between 1 and 5!'
            # Checking CVE
            cve_expression = "^CVE-20[0-9]{2}-[0-9]{4,6}$"
            if regex.search(cve_expression, scenario.cve) is None:
                result['valid_scenario'] = False
                result['message'] = 'Your CVE is in the wrong format or does not exist.\nA CVE must be written in the following format: CVE-YYYY-NNNN'
            # Check the images/containers (we won't check whether the images are valid or nor as this is done in the add | edit image window)
            if scenario.images is None or len(scenario.images) == 0:
                result['valid_scenario'] = False
                result['message'] = 'You need at least one image in your scenario!'             
            return result

        self.scen_to_save.name = self.scenario_name.text()
        self.scen_to_save.description = self.scenario_desc.toPlainText()
        self.scen_to_save.goal = self.goal.toPlainText()
        self.scen_to_save.instructions = self.instructions.toPlainText()
        self.scen_to_save.solution = self.solution.toPlainText()
        self.scen_to_save.cve = self.cve_entry.text()
        self.scen_to_save.difficulty = self.diff_entry.text()
        self.scen_to_save.type = self.type_entry.text()
        self.scen_to_save.sources = [str(source) for source in self.sources.toPlainText().split('\n')]
        is_valid = CheckValid(self.scen_to_save)
        if is_valid['valid_scenario'] is False:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Invalid parameters!")
            messagebox.setText(is_valid['message'])
            messagebox.setStyleSheet('background-color: white')
            messagebox.exec()
        else:
            self.scen_to_save.difficulty = int(self.scen_to_save.difficulty)
            scenarios.Save(self.scen_to_save)
            scenarios_db = scenarios.Load()
            self.scenarios = scenarios_db['scenarios']
            self.list_view.addItem(self.scen_to_save.name)
            self.DefaultMode()
        
        

    # endregion

class EditImagesWindow(QDialog, BaseWindow):
    
    # region =====Initializing=====

    def __init__(self, parent=None, image=None):

        self.parent = parent
        self.image_to_save = self.LoadImageJson(image, self.parent.scen_to_save)

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

    def LoadImageJson(self, wanted_image, scenario):
        if scenario.images is not None:
            for image in scenario.images:
                if wanted_image in image['name']:
                    return image
        else:
            return {}

    def FileDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Select the DockerFile", "", 'All Files (Dockerfile)')

        if fname:
            self.dockerfile_entry.setText(fname[0])

    def FillFields(self):

        # Adding the existing images
        if self.parent.scen_to_save.images is None:
            self.images.addItem('None')
        else:
            self.images.addItem(self.image_to_save['name'])

        for image in self.docker_client.images.list():
            try:
                if self.image_to_save['name'] is not None and self.image_to_save['name'] in image.tags[0].split(':')[0]:
                    continue
            except TypeError:
                pass
            except KeyError:
                pass
            self.images.addItem(image.tags[0])

        # Filling the other fields (or not)
        try:
            if self.image_to_save['is_main'] is True:
                self.is_main.setCurrentText('Yes')
            else:
                self.is_main.setCurrentText('No')
            self.image_os.setText(self.image_to_save['operating_system'])
            for key, value in self.image_to_save['ports'].items():
                self.container_port.setText(key)
                self.host_port.setText(value)
        except TypeError:
            pass
        except KeyError:
            pass

    def SaveImage(self):
        
        def CheckValid(image : dict):
            import regex

            none_not_allowed = ['name', 'is_main', 'operating_system'] # ports are not allowed to be empty either but they will have a special verification
            result = {}
            result['is_valid'] = True

            for key in image:
                if key in none_not_allowed:
                    if image[key] is None or image[key] == "":
                        result['is_valid'] = False
                        result['message'] = f'{key} cannot be empty!'
                if key == 'name':
                    if image[key] == "None" and image['dockerfile'] == "":
                        result['is_valid'] = False
                        result['message'] = 'You need to select either an image or dockerfile!'
                if key == 'ports':
                    if not image[key]:
                        result['is_valid'] = False
                        result['message'] = 'You must enter the container and host ports fields!'
                    else:
                        for _key in image[key]:
                            if _key == "":
                                result['is_valid'] = False
                                result['message'] = 'You must enter the container port!'
                            if image[key][_key] is None or image[key][_key] == "":
                                result['is_valid'] = False
                                result['message'] = 'You must enter the host port!'

            return result

        self.image_to_save['name'] = self.images.currentText()
        self.image_to_save['dockerfile'] = self.dockerfile_entry.text()
        self.image_to_save['is_main'] = True
        if self.is_main.currentText() == "No":
            self.image_to_save['is_main'] = False
        self.image_to_save['ports'] = {}
        self.image_to_save['ports'][self.container_port.text()] = self.host_port.text()
        self.image_to_save['operating_system'] = self.image_os.text()

        is_valid = CheckValid(self.image_to_save)
        if is_valid['is_valid'] is False:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Invalid parameters!")
            messagebox.setText(is_valid['message'])
            messagebox.setStyleSheet('background-color: white')
            messagebox.exec()
        else:
            if self.parent.scen_to_save.images is None or len(self.parent.scen_to_save.images) == 0:
                self.parent.scen_to_save.images = []
                self.parent.scen_to_save.images.append(self.image_to_save)
                self.parent.images_list_view.addItem(self.image_to_save['name'])
            else:
                for image in self.parent.scen_to_save.images:
                    if image['name'] == self.image_to_save['name']:
                        image = self.image_to_save

            self.close()

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())