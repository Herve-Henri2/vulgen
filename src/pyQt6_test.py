import sys
import config
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout

# We first load the graphical parameters from the configuration
configuration = config.Load()
# We then define a few variables from it
width = configuration['main_window_size'][0]
height = configuration['main_window_size'][1]
background_color = configuration['main_window_background_color']
textbox_color = configuration['main_window_textbox_color']
buttons_color = configuration['main_window_buttons_color']
text_color = configuration['text_color']
text_font = configuration['text_font']
text_size = configuration['text_size']

welcome_text = "Welcome to vulgen, our vulnerable environment generator!"

class MainWindow(QWidget):


    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setWindowTitle('Vulnerable environment generator.')
        self.setFixedSize(width, height)
        self.setStyleSheet(f'background-color: {background_color}')

        # Main textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(800,20)
        self.textbox.resize(150,50)

        # Main entry
        self.entry = QLineEdit(self)  
        self.entry.setStyleSheet(f'background-color: {textbox_color}; color: {text_color}; font-family: {text_font}; border: 1px solid "#FFFFFF"')

        # Buttons


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())