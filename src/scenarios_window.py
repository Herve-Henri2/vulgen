from PyQt6.QtWidgets import *
import config
import sys
import scenarios

configuration = config.Load()
scenarios_db = scenarios.Load()

class ScenariosWindow(QDialog):

    scenarios = scenarios_db['scenarios']

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent

        # We define a few graphical variables from the configuration
        self.theme = config.GetTheme(configuration)
        background_color = self.theme['child_window_background_color']
        textbox_color = self.theme['main_window_textbox_color']
        buttons_color = self.theme['buttons_color']
        border_color = self.theme['border_color']
        text_color = self.theme['text_color']
        text_font = self.theme['text_font']
        text_size = self.theme['text_size']

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__(parent)
        self.initUI(background_color, textbox_color, width, height, buttons_color, border_color, text_color, text_font, text_size)


    def initUI(self, background_color, textbox_color, width, height, buttons_color, border_color, text_color, text_font, text_size):

        self.setWindowTitle('Scenarios')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Side ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(200, 400)
        self.list_view.itemClicked.connect(self.showDetails)
        self.list_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")

        # Side TextBox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(240, 20)
        self.textbox.resize(420, 400)
        self.textbox.setReadOnly(True)
        self.textbox.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")

        # Buttons
        self.launch_button = QPushButton('Launch Scenario', self)
        self.launch_button.move(540, 440)
        self.launch_button.resize(120, 20)
        self.launch_button.clicked.connect(self.LaunchScenario)
        self.launch_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.launch_button)

        self.edit_button = QPushButton('Edit Scenario', self)
        self.edit_button.move(400, 440)
        self.edit_button.resize(120, 20)
        self.edit_button.clicked.connect(self.EditMode)
        self.edit_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.DisableButton(self.edit_button)

        self.add_button = QPushButton('Add Scenario', self)
        self.add_button.move(260, 440)
        self.add_button.resize(120, 20)
        self.add_button.clicked.connect(self.AddMode)
        self.add_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

        for scenario in self.scenarios:
            self.list_view.addItem(scenario['name'])

        # Add & Edit mode UI elements
        self.edit_mode_ui = []

        # Buttons
        self.back_button = QPushButton('Back', self)
        self.back_button.move(20, 440)
        self.back_button.resize(80, 20)
        self.back_button.clicked.connect(self.DefaultMode)
        self.back_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.back_button)

        self.save_button = QPushButton('Save', self)
        self.save_button.move(120, 440)
        self.save_button.resize(80, 20)
        self.save_button.clicked.connect(self.SaveScenario)
        self.save_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.save_button)

        self.add_image_button = QPushButton('Add', self)
        self.add_image_button.move(600, 290)
        self.add_image_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.add_image_button)

        self.edit_image_button = QPushButton('Edit', self)
        self.edit_image_button.move(600, 320)
        self.edit_image_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.edit_image_button)
        self.DisableButton(self.edit_image_button)

        self.remove_image_button = QPushButton('Remove', self)
        self.remove_image_button.move(600, 350)
        self.remove_image_button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.remove_image_button)
        self.DisableButton(self.remove_image_button)
        
        # Scenario Name
        self.scenario_name_label = QLabel('Scenario Name', self)
        self.scenario_name_label.move(20, 20)
        self.scenario_name_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.scenario_name_label)

        self.scenario_name = QLineEdit(self)
        self.scenario_name.move(20, 40)
        self.scenario_name.resize(140, 20)
        self.scenario_name.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "{border_color}"')
        self.edit_mode_ui.append(self.scenario_name)

        # Type
        self.type_label = QLabel('Type', self)
        self.type_label.move(180, 20)
        self.type_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.type_label)

        self.type_entry = QLineEdit(self)
        self.type_entry.move(180, 40)
        self.type_entry.resize(140, 20)
        self.type_entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "{border_color}"')
        self.edit_mode_ui.append(self.type_entry)

        # CVE
        self.cve_label = QLabel('CVE', self)
        self.cve_label.move(340, 20)
        self.cve_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.cve_label)

        self.cve_entry = QLineEdit(self)
        self.cve_entry.move(340, 40)
        self.cve_entry.resize(140, 20)
        self.cve_entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "{border_color}"')
        self.edit_mode_ui.append(self.cve_entry)

        # Description
        self.scenario_desc_label = QLabel('Description', self)
        self.scenario_desc_label.move(20, 80)
        self.scenario_desc_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.scenario_desc_label)

        self.scenario_desc = QPlainTextEdit(self)
        self.scenario_desc.move(20, 100)
        self.scenario_desc.resize(300, 150)
        self.scenario_desc.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}'")
        self.edit_mode_ui.append(self.scenario_desc)

        # Instructions
        self.instructions_label = QLabel('Instructions', self)
        self.instructions_label.move(340, 80)
        self.instructions_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.instructions_label)

        self.instructions = QPlainTextEdit(self)
        self.instructions.move(340, 100)
        self.instructions.resize(300, 150)
        self.instructions.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}'")
        self.edit_mode_ui.append(self.instructions)

        # Goal
        self.goal_label = QLabel('Goal', self)
        self.goal_label.move(20, 270)
        self.goal_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.goal_label)

        self.goal = QPlainTextEdit(self)
        self.goal.move(20, 290)
        self.goal.resize(300, 40)
        self.goal.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}'")
        self.edit_mode_ui.append(self.goal)

        # Sources
        self.sources_label = QLabel('Sources', self)
        self.sources_label.move(20, 350)
        self.sources_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.sources_label)

        self.sources = QPlainTextEdit(self)
        self.sources.move(20, 370)
        self.sources.resize(300, 40)
        self.sources.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}'")
        self.edit_mode_ui.append(self.sources)

        # Images
        self.images_label = QLabel('Images', self)
        self.images_label.move(340, 270)
        self.images_label.setStyleSheet(f'color: {text_color}; font-family: {text_font}')
        self.edit_mode_ui.append(self.images_label)

        self.images_list_view = QListView(self)
        self.images_list_view.move(340, 290)
        self.images_list_view.resize(250, 120)
        self.images_list_view.setStyleSheet(f"background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; font-size: {text_size};  border: 1px solid '{border_color}';")
        self.edit_mode_ui.append(self.images_list_view)

        #self.HideEditUI()
        self.AddMode()



    # endregion

    # region =====Graphical Methods=====

    def setText(self, text : str):
        self.textbox.setPlainText(text)

    def showDetails(self):
        for scenario in self.scenarios:
            if scenario['name'] == self.list_view.currentItem().text():
                self.setText(scenario['description']
                            +f"\n-----------------------------\nGoal: {scenario['goal']}"
                            +f"\n-----------------------------\nType: {scenario['type']}"
                            +f"\n-----------------------------\nCVE: {scenario['CVE']}")
        self.EnableButton(self.launch_button)
        self.EnableButton(self.edit_button)

    def DisableButton(self, button : QPushButton):
        buttons_color = self.theme['disabled_buttons_color']
        text_color = self.theme['disabled_text_color']
        text_font = self.theme['text_font']

        button.setEnabled(False)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font};')

    def EnableButton(self, button : QPushButton):
        buttons_color = self.theme['buttons_color']
        text_color = self.theme['text_color']
        text_font = self.theme['text_font']

        button.setEnabled(True)
        button.setStyleSheet(f'background-color: {buttons_color}; color: {text_color}; font-family: {text_font}')

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
        self.DisableButton(self.launch_button)
        self.DisableButton(self.edit_button)
        self.DisableButton(self.add_button)
        self.textbox.hide()
        self.list_view.hide()
        self.ShowEditUI()

        selected_scenario = self.list_view.currentItem().text()

    def AddMode(self):
        # Setting up the UI
        self.DisableButton(self.launch_button)
        self.DisableButton(self.edit_button)
        self.DisableButton(self.add_button)
        self.textbox.hide()
        self.list_view.hide()
        self.ShowEditUI()

    def DefaultMode(self):
        '''
        Resets the window's UI back to default.
        '''
        self.HideEditUI()
        self.EnableButton(self.add_button)
        self.textbox.show()
        self.list_view.show()

    def SaveScenario(self):
        #TODO Check all the inputs!
        pass
        
        

    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScenariosWindow()
    ex.show()
    sys.exit(app.exec())