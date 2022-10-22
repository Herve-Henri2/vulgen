import tkinter
import config

# We first load the graphical parameters from the configuration
configuration = config.Load()
# We then define a few variables from it
width = configuration['main_window_size'][0]
height = configuration['main_window_size'][1]
background_color = configuration['main_window_background_color']
textbox_color = configuration['main_window_textbox_color']
buttons_color = configuration['main_window_buttons_color']
text_color = configuration['text_color']

class main_window(tkinter.Tk):
    
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_pos = int((screen_width/2) - (width/2))
        y_pos = int((screen_height/2) - (height/2))

        self.title('Vulnerable Environment Generator')
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.resizable(width=False, height=False)
        self.configure(bg=background_color)

if __name__ == "__main__":
    test = main_window()
    test.mainloop()

        
