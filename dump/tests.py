# File made for testing purposes.
try:
    import win32gui, win32con
    import win32com.client
except:
    pass
import os
import tkinter
import psutil
import subprocess
import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


def minimize_top_window():
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)


def see_all_processes():
    for proc in psutil.process_iter():
        print(proc)


def see_all_windows():
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print (hex(hwnd), win32gui.GetWindowText( hwnd ))

    win32gui.EnumWindows( winEnumHandler, None )

def test_close_window():

    window_name = 'Docker Desktop'

    def close_window(hwnd, ctx):
        if win32gui.IsWindowVisible( hwnd ):
            if window_name.lower() in win32gui.GetWindowText(hwnd).lower():
                win32gui.ShowWindow(hwnd, False)

    win32gui.EnumWindows( close_window, None )

def find_window_by_name():
    name = 'Images - Docker Desktop'
    whnd = win32gui.FindWindowEx(None, None, None, name)
    if not (whnd == 0):
        print('found! Killing it now!')
        win32gui.ShowWindow(whnd, False)
    else:
        print('not found!')

def test_json():
    file_name = 'testy.json'
    _json = {}
    _json['First'] = first = {}
    first['second'] = '5'
    first['third'] = third = {}
    third['test'] = 'chelo'
    third['testo'] = 'chela'
    #print(json.dumps(_json, indent=3))
    with open (file_name, 'w') as file:
        file.write(json.dumps(_json))

def open_terminal(_os, command=None):
    if _os == "Windows":
        if not command:
            command = "cmd.exe"
        with open("terminal.bat", "w") as file:
            file.write("@echo off\n"
                       "color 09\n"
                       f"powershell {command}")
        subprocess.call('terminal.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif _os == "Linux":
        if not command:
            command = "exec bash"
        os.system(f"gnome-terminal -e 'bash -c \"{command}\"'")
        #os.system("gnome-terminal -e 'bash -c \"sudo apt-get update; exec bash\"'")


class App(tk.Tk):
  def __init__(self):
    super().__init__()

    width = 950; height = 600
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    self.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))
    # configure the root window
    self.title('My Awesome App')
    # self.minsize(950, 600)
    self.resizable(width=False, height=False)
    # self.eval('tk::PlaceWindow . center')

    # label
    self.label = ttk.Label(self, text='Hello, Tkinter!')
    self.label.pack()

    # button
    self.button = ttk.Button(self, text='Click Me')
    self.button['command'] = self.button_clicked
    self.button.pack()

  def button_clicked(self):
    showinfo(title='Information', message='Hello, Tkinter!')

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
