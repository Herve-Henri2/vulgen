import sys

from application import *
import docker_utils as dutils
from scenarios import *

# region =====Scenario Window=====

class ScenariosWindow(QDialog, BaseWindow):
    # region =====Initializing=====

    def __init__(self, parent=None):
        self.parent = parent
        self.scenarios : dict[str, Scenario] = scenarios_db['scenarios']
        self.current_scenario_containers = dict[str, Container]()

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
        
        self.remove_button = QPushButton('Remove Scenario', self)
        self.remove_button.move(400, 470)
        self.remove_button.resize(120, 20)
        self.remove_button.clicked.connect(self.RemoveScenario)
        self.default_mode_ui.append(self.remove_button)

        self.add_button = QPushButton('Add Scenario', self)
        self.add_button.move(260, 440)
        self.add_button.resize(120, 20)
        self.add_button.clicked.connect(self.AddScenarioMode)
        self.default_mode_ui.append(self.add_button)

        self.RefreshListView()

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

        self.add_container_button = QPushButton('Add', self)
        self.add_container_button.move(600, 290)
        self.add_container_button.clicked.connect(self.OpenContainerAdd)
        self.edit_mode_ui.append(self.add_container_button)

        self.edit_container_button = QPushButton('Edit', self)
        self.edit_container_button.move(600, 320)
        self.edit_container_button.clicked.connect(self.OpenContainerEdit)
        self.edit_mode_ui.append(self.edit_container_button)

        self.remove_container_button = QPushButton('Remove', self)
        self.remove_container_button.move(600, 350)
        self.remove_container_button.clicked.connect(self.RemoveContainer)
        self.edit_mode_ui.append(self.remove_container_button)
        
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
        self.solution_label.move(340, 80)
        self.edit_mode_ui.append(self.solution_label)

        self.solution = QPlainTextEdit(self)
        self.solution.move(340, 100)
        self.solution.resize(300, 150)
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

        # Containers
        self.containers_label = QLabel('Containers', self)
        self.containers_label.move(340, 270)
        self.edit_mode_ui.append(self.containers_label)

        self.containers_list_view = QListWidget(self)
        self.containers_list_view.move(340, 290)
        self.containers_list_view.resize(250, 120)
        self.containers_list_view.itemClicked.connect(self.AllowOpening)
        self.edit_mode_ui.append(self.containers_list_view)

        self.HideUIElements(self.edit_mode_ui)

        # Styling and coloring
        self.ImplementTheme()
        self.DisableButtons(self.edit_button, self.launch_button, self.remove_button, 
        self.edit_container_button, self.remove_container_button)

    # endregion

    # region =====Graphical Methods=====

    def showDetails(self):
        scenario_name = self.list_view.currentItem().text()
        scenario = self.scenarios[scenario_name]
        self.setText(scenario.description
                    +f"\n-----------------------------\nGoal: {scenario.goal}"
                    +f"\n-----------------------------\nType: {scenario.type}"
                    +f"\n-----------------------------\nCVE: {scenario.CVE}"
                    +f"\n-----------------------------\nDifficulty: {scenario.difficulty}")
        self.EnableButtons(self.launch_button, self.edit_button, self.remove_button)
    
    def AllowOpening(self):
        self.EnableButtons(self.edit_container_button, self.remove_container_button)

    def HideUIElements(self, ui_elements):
        for element in ui_elements:
            element.hide()

    def ShowUIElements(self, ui_elements):
        for element in ui_elements:
            element.show()
    
    def RefreshListView(self):
        self.list_view.clear()
        for scenario_name in self.scenarios:
            self.list_view.addItem(scenario_name)

    def OpenContainerAdd(self):
        window = EditContainersWindow(parent=self, addingMode=True)
        window.exec()

    def OpenContainerEdit(self):
        selected_container_name = self.containers_list_view.currentItem().text().replace('(main) ', '')
        selected_container = self.current_scenario_containers[selected_container_name]
        window = EditContainersWindow(parent=self, container_to_edit=selected_container)
        window.exec()

    def RemoveContainer(self):
        messagebox = QMessageBox(self)
        messagebox.setStyleSheet('background-color: blue')
        remove = messagebox.question(self, 'Removing container', 'Are you sure you want to remove that container from the scenario?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if remove == QMessageBox.StandardButton.Yes:
            scenario_name = self.containers_list_view.currentItem().text().replace("(main) ", "")
            self.containers_list_view.takeItem(self.containers_list_view.currentRow())
            self.current_scenario_containers.pop(scenario_name)

    # endregion

    # region =====Main Methods=====

    def LaunchScenario(self):
        scenario_name = self.list_view.currentItem().text()
        self.parent.LaunchScenario(scenario_name)
        self.close()
    
    def RemoveScenario(self):
        messagebox = QMessageBox(self)
        messagebox.setStyleSheet('background-color: blue')
        remove = messagebox.question(self, 'Removing scenario', 'Are you sure you want to remove that scenario?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if remove == QMessageBox.StandardButton.Yes:
            scenario_name = self.list_view.currentItem().text()
            # Remove scenario folder
            Remove(scenario_name)
            # Update scenarios_db and self.scenarios
            scenarios_db = scenarios.Load()
            self.scenarios = scenarios_db['scenarios']
            # Update List View
            self.RefreshListView()
            # Clear the textbox
            self.Clear()

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
        self.cve_entry.setText(scenario.CVE)
        self.diff_entry.setText(str(scenario.difficulty))
        self.scenario_desc.setPlainText(scenario.description)
        self.solution.setPlainText(scenario.solution)
        self.goal.setPlainText(scenario.goal)
        for source in scenario.sources:
            self.sources.appendPlainText(source)
        for container in scenario.containers.values():
            self.current_scenario_containers[container.image_name] = container
            self.containers_list_view.addItem(f"(main) {container.image_name}") if container.is_main is True else self.containers_list_view.addItem(container.image_name)
                

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
        self.DisableButtons(self.edit_button, self.launch_button, self.remove_button,
        self.edit_container_button, self.remove_container_button)
        self.current_scenario_containers.clear()
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
            elif not name[0].isalnum():
                result['valid_scenario'] = False
                result['message'] += f'The first character of the name must be an alphanumeric character [a-zA-Z0-9]!'
            
            # CVE
            cve = self.cve_entry.text()
            if(len(cve) != 0):
                cve_expression = "^CVE-20[0-9]{2}-[0-9]{4,6}$"
                if regex.search(cve_expression, cve) is None:
                    result['valid_scenario'] = False
                    result['message'] += 'Your CVE is in the wrong format.\nA CVE must be written in the following format: CVE-YYYY-NNNN' + '\n'

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
            
            # Containers
            if self.containers_list_view.count() == 0:
                result['valid_scenario'] = False
                result['message'] += 'You need at least one container in your scenario!' + '\n'
            
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
            scenario_to_save.name = self.scenario_name.text().replace(' ', '_')
            scenario_to_save.description = self.scenario_desc.toPlainText()
            scenario_to_save.goal = self.goal.toPlainText()
            scenario_to_save.solution = self.solution.toPlainText()
            scenario_to_save.CVE = self.cve_entry.text()
            scenario_to_save.difficulty = self.diff_entry.text()
            scenario_to_save.type = self.type_entry.text()
            scenario_to_save.sources = [str(source) for source in self.sources.toPlainText().split('\n') if len(source) > 0]
            scenario_to_save.containers = self.current_scenario_containers
            
            scenarios.Save(scenario_to_save)
            scenarios_db = scenarios.Load()
            self.scenarios = scenarios_db['scenarios']
            self.RefreshListView()
            self.DefaultMode()
            self.Clear()
        

    # endregion

# endregion

# region =====EditContainersWindow=====

class EditContainersWindow(QDialog, BaseWindow):
    
    # region =====Initializing=====

    def __init__(self, parent = None, addingMode = False, container_to_edit : Container = None):

        self.parent = parent
        self.addingMode = addingMode
        if self.addingMode is False:
            self.container_to_edit = container_to_edit

        # Defining our layout variables
        width = 600
        height = 500

        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):
        self.setWindowTitle('Add | Edit scenario container')
        self.setFixedSize(width, height)

        # Image
        self.image_label = QLabel('From Image', self)
        self.image_label.move(20, 20)

        self.image_entry = QLineEdit(self)
        self.image_entry.move(20, 40)
        self.image_entry.resize(300, 20)

        # Dockerfile
        self.dockerfile_label = QLabel('From Dockerfile', self)
        self.dockerfile_label.move(20, 20)

        self.dockerfile_entry = QLineEdit(self)
        self.dockerfile_entry.move(20, 40)
        self.dockerfile_entry.resize(300, 20)
        self.dockerfile_entry.setEnabled(False)
        
        # Networks
        self.networks_label = QLabel('Networks', self)
        self.networks_label.move(20, 110)
        
        self.networks_entry = QLineEdit(self)
        self.networks_entry.move(20, 130)
        self.networks_entry.resize(140, 20)

        self.networks = QListWidget(self)
        self.networks.move(20, 160)
        self.networks.resize(210, 150)
        self.networks.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)        
        
        # Container port
        self.container_port_label = QLabel('Container port', self)
        self.container_port_label.move(280, 160)

        self.container_port = QLineEdit(self)
        self.container_port.move(280, 180)
        self.container_port.resize(100, 20)
        
        # Host port
        self.host_port_label = QLabel('Host port', self)
        self.host_port_label.move(400, 160)

        self.host_port = QLineEdit(self)
        self.host_port.move(400, 180)
        self.host_port.resize(100, 20)
        
        # Operating System
        self.container_os_label = QLabel('Operating system', self)
        self.container_os_label.move(280, 210)

        self.container_os = QLineEdit(self)
        self.container_os.move(280, 230)
        self.container_os.resize(150, 20)
        
        # Buttons
        self.save_button = QPushButton('Save', self)
        self.save_button.move(20, 440)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.SaveContainer)

        self.image_browse_button = QPushButton('Browse', self)
        self.image_browse_button.move(20, 70)
        self.image_browse_button.resize(80, 20)
        self.image_browse_button.clicked.connect(self.ImageDialog)
        
        self.dockerfile_browse_button = QPushButton('Browse', self)
        self.dockerfile_browse_button.move(20, 70)
        self.dockerfile_browse_button.resize(80, 20)
        self.dockerfile_browse_button.clicked.connect(self.FileDialog)
        
        self.network_add_button = QPushButton('Add', self)
        self.network_add_button.move(170, 130)
        self.network_add_button.resize(40, 20)
        self.network_add_button.clicked.connect(self.AddNetworkChoice)
        
        # Checkboxes
        self.image_checkbox_label = QLabel("Image", self)
        self.image_checkbox_label.move(360, 40)  
        self.image_checkbox = QCheckBox(self)
        self.image_checkbox.move(405, 38)
        self.image_checkbox.resize(20, 20)
        self.image_checkbox.setChecked(True)
        self.image_checkbox.stateChanged.connect(self.onCheck)
        
        self.dockerfile_checkbox_label = QLabel("Dockerfile", self)
        self.dockerfile_checkbox_label.move(460, 40)
        self.dockerfile_checkbox = QCheckBox(self)
        self.dockerfile_checkbox.move(520, 38)
        self.dockerfile_checkbox.resize(20, 20)
        self.dockerfile_checkbox.stateChanged.connect(self.onCheck)        

        self.is_main_checkbox_label = QLabel('Main Container', self)
        self.is_main_checkbox_label.move(280, 130)
        self.is_main_checkbox = QCheckBox(self)
        self.is_main_checkbox.move(370, 128)
        self.is_main_checkbox.resize(20, 20)

        self.requires_it_label = QLabel('Requires Interaction', self)
        self.requires_it_label.move(400, 130)
        self.requires_it_checkbox = QCheckBox(self)
        self.requires_it_checkbox.move(520, 128)
        self.requires_it_checkbox.resize(20, 20)

        self.ImplementTheme()

        self.checkBoxGroup = QButtonGroup(self)
        self.checkBoxGroup.addButton(self.image_checkbox); self.checkBoxGroup.addButton(self.dockerfile_checkbox)
        
        self.dockerfile_label.hide(); self.dockerfile_entry.hide(); self.dockerfile_browse_button.hide()

        self.FillFields()

    # endregion

    # region =====Graphical Methods=====

    def onCheck(self):
        if self.image_checkbox.isChecked():
            self.image_label.show(); self.image_entry.show(); self.image_browse_button.show()
            self.dockerfile_label.hide(); self.dockerfile_entry.hide(); self.dockerfile_browse_button.hide()
        elif self.dockerfile_checkbox.isChecked():
            self.dockerfile_label.show(); self.dockerfile_entry.show(); self.dockerfile_browse_button.show()
            self.image_label.hide(); self.image_entry.hide(); self.image_browse_button.hide()
        
    def AddNetworkChoice(self):
        new_choice = self.networks_entry.text()
        if not self.networks.findItems(new_choice, Qt.MatchFlag.MatchFixedString | Qt.MatchFlag.MatchCaseSensitive):
            self.networks.addItem(new_choice)
    
    # endregion

    # region =====Main Methods=====
    def ImageDialog(self):
        images = [image.tags[0] for image in self.docker_client.images.list()]
        non_custom_images = [image for image in images if image.split(':')[1] != "custom"]
        
        if len(non_custom_images) != 0:
            # TODO implement style on it
            image, ok = QInputDialog.getItem(self, "Image input", "List of non custom images:", non_custom_images, 0, False)
            if ok and image:            
                self.image_entry.setText(image)
        else:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Error")
            messagebox.setText("No images available!")
            messagebox.exec()
    
    def FileDialog(self):
        custom_images_path = src_folder_path + f"{sep}..{sep}docker_images"
        fname = QFileDialog.getExistingDirectory(self, caption="Select the DockerFile folder", directory=custom_images_path)
        if fname:
            project_folder_path = src_folder_path[:src_folder_path.rfind(sep)]
            fname = fname.replace(project_folder_path, "..")
            self.dockerfile_entry.setText(fname)

    def FillFields(self):        
        # Filling the networks
        existing_networks = [network.name for network in self.docker_client.networks.list()]
        if self.addingMode is False:
            existing_networks.extend(self.container_to_edit.networks)
            all_networks = set(existing_networks)
            self.networks.addItems(all_networks)            
            
            for i in range(self.networks.count()):
                if self.networks.item(i).text() in self.container_to_edit.networks:
                    self.networks.item(i).setSelected(True)   
        else:            
            self.networks.addItems(existing_networks)
            for i in range(self.networks.count()):
                if self.networks.item(i).text() == "bridge":
                    self.networks.item(i).setSelected(True)
                    break

        # Filling the other fields (or not)
        if self.addingMode is False:
            self.container_os.setText(self.container_to_edit.operating_system)
            
            if len(self.container_to_edit.dockerfile) != 0:
                self.dockerfile_checkbox.setChecked(True)
                self.dockerfile_entry.setText(self.container_to_edit.dockerfile)
            else:
                self.image_entry.setText(self.container_to_edit.image_name)
            
            if self.container_to_edit.is_main is True:
                self.is_main_checkbox.setChecked(True)

            if self.container_to_edit.requires_it is True:
                self.requires_it_checkbox.setChecked(True)
                
            for key, value in self.container_to_edit.ports.items():
                self.container_port.setText(key)
                self.host_port.setText(value)

    def SaveContainer(self):
        
        def CheckValid():
            result = {}
            result['is_valid'] = True
            result['message'] = ""
            
            # Image Name & Dockerfile
            image_name = self.image_entry.text()
            dockerfile = self.dockerfile_entry.text()
            if len(image_name) == 0 and len(dockerfile) == 0:
                result['is_valid'] = False
                result['message'] += 'You need to have either an image or a dockerfile!\n' 
            
            # Ports
            ports = (self.container_port.text(), self.host_port.text())
            if len(ports[0]) != 0 or len(ports[1]) != 0:
                if not ports[0].isdigit() or not ports[1].isdigit():
                    result['is_valid'] = False
                    result['message'] += 'If specified, the ports number must be positive integers!\n'                    

            return result

        is_valid = CheckValid()
        if is_valid['is_valid'] is False:
            messagebox = QMessageBox(self)
            messagebox.setWindowTitle("Invalid parameters!")
            messagebox.setText(is_valid['message'])
            messagebox.setStyleSheet('background-color: white; color: black')
            messagebox.exec()
        else:
            container_to_save = Container()
            
            if self.dockerfile_checkbox.isChecked():
                container_to_save.dockerfile = self.dockerfile_entry.text()
                container_to_save.image_name = f"{container_to_save.dockerfile.split('/')[-1]}:custom"
            else:
                container_to_save.image_name = self.image_entry.text()
                
            container_to_save.is_main = self.is_main_checkbox.isChecked()
            container_to_save.requires_it = self.requires_it_checkbox.isChecked()
            container_to_save.networks = [selection.text() for selection in self.networks.selectedItems()]
            if len(self.container_port.text()) != 0 and len(self.host_port.text()) != 0:
                container_to_save.ports = {self.container_port.text() : self.host_port.text()}
            container_to_save.operating_system = self.container_os.text()
            
            self.parent.current_scenario_containers[container_to_save.image_name] = container_to_save
            if self.addingMode is True:
                if container_to_save.is_main:
                    self.parent.containers_list_view.addItem(f"(main) {container_to_save.image_name}")
                else:
                    self.parent.containers_list_view.addItem(container_to_save.image_name)
            else:
                image_name_changed = self.container_to_edit.image_name != container_to_save.image_name
                                
                for i in range(self.parent.containers_list_view.count()):
                    item = self.parent.containers_list_view.item(i)
                    if item.text().replace("(main) ", "") == self.container_to_edit.image_name:
                        if container_to_save.is_main:
                            item.setText(f"(main) {container_to_save.image_name}")
                        else:
                            item.setText(container_to_save.image_name)
                        break
                if image_name_changed:
                    self.parent.current_scenario_containers.pop(self.container_to_edit.image_name)

            self.close()

    # endregion

# endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())