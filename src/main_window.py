from cgitb import text
import tkinter as tk
from tkinter import ttk
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
text_font = configuration['text_font']
text_size = configuration['text_size']

welcome_text = "Welcome to vulgen, our vulnerable environment generator!"

class main_window(tk.Tk):
    
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

        # Main textbox 
        self.textbox = tk.Text(height=28, width=90, bg=textbox_color, fg=text_color, borderwidth=0, font=(text_font, text_size))
        self.textbox.place(x=180, y=20)
        self.SetText(welcome_text)

        # Main entry, we will use another textbox for it
        self.entry = tk.Text(height=3, width=90, bg=textbox_color, fg=text_color, borderwidth=0, font=(text_font, text_size, "italic"))
        self.entry.place(x=180, y=460)
        self.entry.insert(tk.END, 'Replace this text then click on the Enter button to enter your input.')

        # Enter Button
        self.enter_button = tk.Button(height=1, width=10, background=buttons_color, foreground=text_color, borderwidth=0.9, text='Enter',
                                      command=self.GetUserInput)
        self.enter_button.place(x=735, y=530)

        # Bindings
        self.bind('<Return>', lambda event: self.GetUserInput())

    def GetUserInput(self):
        '''
        Returns the text that the user wrote in the entry textbox, then wipes it.
        '''
        text = self.entry.get("1.0", "end-1c")
        self.entry.delete(1.0, tk.END)
        return text

    def Write(self, text):
        '''
        Appends the specified text to the current textbox's one.
        '''
        self.textbox.configure(state='normal')
        self.textbox.insert(tk.END, text)
        self.textbox.configure(state='disabled')

    def SetText(self, text):
        '''
        Overwrites the textbox's text with the one specified.
        '''
        self.textbox.configure(state='normal')
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, text)
        self.textbox.configure(state='disabled')

if __name__ == "__main__":
    test = main_window()
    test.mainloop()

        
