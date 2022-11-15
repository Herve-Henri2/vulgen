import sys

from base_window import *
import scenarios


class ScenariosWindow(QDialog, BaseWindow):

    scenarios_db = scenarios.Load()
    scenarios = scenarios_db['scenarios']

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent

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
        self.edit_button.clicked.connect(self.EditMode)

        self.add_button = QPushButton('Add Scenario', self)
        self.add_button.move(260, 440)
        self.add_button.resize(120, 20)
        self.add_button.clicked.connect(self.AddMode)

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
        self.edit_mode_ui.append(self.add_image_button)

        self.edit_image_button = QPushButton('Edit', self)
        self.edit_image_button.move(600, 320)
        self.edit_mode_ui.append(self.edit_image_button)

        self.remove_image_button = QPushButton('Remove', self)
        self.remove_image_button.move(600, 350)
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
        self.instructions.resize(300, 150)
        self.edit_mode_ui.append(self.instructions)

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

    # endregion

    # region =====Main Methods=====

    def LaunchScenario(self):
        scenario = self.list_view.currentItem().text()
        self.parent.LaunchScenario(scenario)
        self.close()

    def EditMode(self):
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
        scenario = scenarios.LoadScenario(selected_scenario)
        self.scenario_name.setText(scenario.name)
        self.type_entry.setText(scenario.type)
        self.cve_entry.setText(scenario.cve)
        self.scenario_desc.setPlainText(scenario.description)
        self.instructions.setPlainText(scenario.instructions)
        self.goal.setPlainText(scenario.goal)
        for source in scenario.sources:
            self.sources.appendPlainText(source)
        for image in scenario.images:
            if image['is_main'] is True:
                self.images_list_view.addItem(f"(main) {image['name']}")
            else:
                self.images_list_view.addItem(image['name'])

    def AddMode(self):
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
        self.HideEditUI()
        self.ShowElements(self.launch_button, self.edit_button, self.add_button,
        self.textbox, self.list_view)
        self.DisableButtons(self.edit_button, self.launch_button)
        for element in self.edit_mode_ui:
            if isinstance(element, QLineEdit) or isinstance(element, QPlainTextEdit) or isinstance(element, QListWidget):
                element.clear()

    def SaveScenario(self):
        #TODO Check all the inputs!
        pass
        
        

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())