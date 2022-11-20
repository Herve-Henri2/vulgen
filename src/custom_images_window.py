import os
import subprocess
import sys

from application import *
import docker_utils as dutils

class CustomImagesWindow(QDialog, BaseWindow):

    # region =====Initializing=====

    def __init__(self, parent=None):

        self.parent = parent

        # Defining our layout variables
        width = 700
        height = 500

        super().__init__()
        self.initUI(width, height)


    def initUI(self, width, height):

        self.setWindowTitle('Custom Images')
        self.setFixedSize(width, height)

        # ListView
        self.list_view = QListWidget(self)
        self.list_view.move(40, 20)
        self.list_view.resize(620, 400)
        self.list_view.itemClicked.connect(self.ImageClicked)
        self.list_view.itemDoubleClicked.connect(self.BuildImage)

        # Buttons
        self.build_button = QPushButton('Build Image', self)
        self.build_button.move(290, 450)
        self.build_button.resize(120, 20)
        self.build_button.clicked.connect(self.BuildImage)
        #self.DisableButton(self.build_button)
        
        # Fill the table
        self.updateList()
        # Styling and coloring
        self.ImplementTheme()
            
    # endregion

    # region =====Graphical Methods=====

    def ImageClicked(self):
        self.EnableButton(self.build_button)
    
    def updateList(self):        
        img_list = dutils.GetCustomImages()
        
        self.list_view.addItems(img_list)

    # endregion

    # region =====Main Methods=====

    def BuildImage(self):
        #TODO add Windows compatibility
        selection = self.list_view.currentItem().text()
        try:
            sep = '/' if operating_system == "Linux" else '\\'
            custom_images_path = os.path.realpath(os.path.dirname(__file__)) + f"{sep}..{sep}docker_images"  # src folder absolute path + path to docker_images from src folder
            docker_file_path = f'{custom_images_path}{sep}{selection}'
            self.docker_client.images.build(path=docker_file_path, rm=True)
            self.parent.setText(f'Successfully built the {selection} image!')
            logger.info(f'Built the {selection} image.')
            #subprocess.Popen(f'{custom_images_path}\\{selection}\\create_img.sh')
            #command = f"cd {path}\\{selection}\\create_img.sh"
            #misc.open_terminal(configuration['operating_system'], command=command)
        except Exception as ex:
            self.parent.setText(str(ex))
            logger.error(f'An error occured while trying to build the image {selection}: {ex}')
        finally:
            self.close()
        
    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CustomImagesWindow()
    ex.show()
    sys.exit(app.exec())
