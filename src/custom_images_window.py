import os
import subprocess
import sys

from application import *
import docker_utils as dutils

class CustomImagesWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent
        self.selected_image = None
        self.selected_image_type = None

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)


    def initUI(self, width, height):

        self.setWindowTitle('Custom Images')
        self.setFixedSize(width, height)

        # Base images
        self.base_images_label = QLabel('Base images', self)
        self.base_images_label.move(40, 20)

        self.base_images = QListWidget(self)
        self.base_images.move(40, 40)
        self.base_images.resize(620, 80)
        self.base_images.itemClicked.connect(self.BaseImageClicked)
        self.base_images.itemDoubleClicked.connect(self.BuildImage)

        # Scenario images
        self.scenario_images_label = QLabel('Scenario images', self)
        self.scenario_images_label.move(40, 140)

        self.scenario_images = QListWidget(self)
        self.scenario_images.move(40, 160)
        self.scenario_images.resize(620, 120)
        self.scenario_images.itemClicked.connect(self.ScenImageClicked)
        self.scenario_images.itemDoubleClicked.connect(self.BuildImage)

        # Other images
        self.misc_images_label = QLabel('Miscellaneous images', self)
        self.misc_images_label.move(40, 300)

        self.misc_images = QListWidget(self)
        self.misc_images.move(40, 320)
        self.misc_images.resize(620, 80)
        self.misc_images.itemClicked.connect(self.MiscImageClicked)
        self.misc_images.itemDoubleClicked.connect(self.BuildImage)

        # Buttons
        self.build_button = QPushButton('Build Image', self)
        self.build_button.move(290, 450)
        self.build_button.resize(120, 20)
        self.build_button.clicked.connect(self.BuildImage)
        
        # Fill the table
        self.updateLists()
        # Styling and coloring
        self.ImplementTheme()
        self.DisableButton(self.build_button)
            
    # endregion

    # region =====Graphical Methods=====

    def BaseImageClicked(self):
        self.EnableButton(self.build_button)
        self.selected_image = self.base_images.currentItem().text()
        self.selected_image_type = "base"

        # Updating the selection (deselecting from other list views)
        self.scenario_images.clearSelection()
        self.misc_images.clearSelection()
        
    def ScenImageClicked(self):
        self.EnableButton(self.build_button)
        self.selected_image = self.scenario_images.currentItem().text()
        self.selected_image_type = "scenario"

        # Updating the selection (deselecting from other list views)
        self.base_images.clearSelection()
        self.misc_images.clearSelection()

    def MiscImageClicked(self):
        self.EnableButton(self.build_button)
        self.selected_image = self.misc_images.currentItem().text()
        self.selected_image_type = "misc"

        # Updating the selection (deselecting from other list views)
        self.base_images.clearSelection()
        self.scenario_images.clearSelection()

  
    def updateLists(self):
        '''
        Fills in all of our list views with the adequate images.
        '''
        custom_images = dutils.GetCustomImages()  

        base_img_list = custom_images[0]     
        scenario_img_list = custom_images[1]
        misc_img_list = custom_images[2] 

        self.base_images.addItems(base_img_list)
        self.scenario_images.addItems(scenario_img_list)
        self.misc_images.addItems(misc_img_list)

    # endregion

    # region =====Main Methods=====

    def BuildImage(self):
        '''
        Closes this window to call the BuildCustomImage() function of its parent.
        '''
        dockerfiles_path = dutils.GetImageRequirements(self.selected_image, self.selected_image_type)
        self.parent.BuildCustomImage(dockerfiles_path)
        self.close()
        
    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CustomImagesWindow()
    ex.show()
    sys.exit(app.exec())