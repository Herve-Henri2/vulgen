import subprocess
import psutil
import os
from PyQt6.QtWidgets import *
try:
    import win32gui
except ModuleNotFoundError:
    pass

def unallowWindowOpening(window_name, done=False):
    '''
    Waits for the specified window to open up to immediately close it.
    '''
    while not done:
        foreground_window = win32gui.GetForegroundWindow()
        if win32gui.GetWindowText(foreground_window) == window_name:
            win32gui.ShowWindow(foreground_window, False)
            done = True

def ProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def DisplayList(enum):
    '''
    Displays the elements of an enumerable (one element per line).
    '''
    for element in enum:
        print(element)


def error(msg = "Error!"):
    print(f"\nError : {msg}\n")


def open_terminal(_os="Linux", command=None, insta_exit=True):
    '''
    Opens up a terminal (or command prompt).
    ---------------
    Parameters:
    
    _os : str ->
    The machine's operating system

    command: str ->
    The command to be executed after the terminal's opening

    insta_exit: boolean ->
    If set to True, the terminal will instantly close once the command has been completed.
    '''
    
    if _os == "Windows":
        if command is None:
            command = "cmd.exe"
        with open("terminal.bat", "w") as file:
            if insta_exit:
                file.write("@echo off\n"
                        "color 09\n"
                        f"powershell {command}\n")
            else:
                file.write("@echo off\n"
                        "color 09\n"
                        f"powershell -NoExit {command}\n")
        subprocess.Popen('terminal.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif _os == "Linux":
        if command is None:
            command = "exec bash -i"
        if insta_exit:
            os.popen(f"gnome-terminal -- bash -c \"{command};exit;\"")
        else:
            os.popen(f"gnome-terminal -- bash -c \"{command}\"")


def StyleSheetTest():

    original = "background-color: #050505; color: #CF0000; font-family: Walbaum Display; font-size: 12;  border: 1px solid '#CF0000'"

    def extractBorder():
        border_part = original.split(';')[-1].strip()
        original_no_border = ';'.join(original.split(';')[:-1])
        border_color = border_part[-8:].replace("'", "")
        new_color = "#888888"
        new_stylesheet = f"{original_no_border}; border: 1px solid '{new_color}'"
        test = original.split(';')[-1].strip()[-8:].replace("'", "")
        print(border_part)
        print(border_color)
        print(new_stylesheet)
        print(test)


    extractBorder()


if __name__ =="__main__":
    #open_terminal("Windows")
    StyleSheetTest()
