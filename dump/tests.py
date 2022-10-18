# File made for testing purposes.
from pickle import TRUE
import win32gui, win32con
import win32com.client
import os
import psutil
import subprocess
import json
import platform

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
        pass

def main():
    open_terminal("Windows", "docker exec -it e08ab8acbf9d57a705537be1ead0b86408b3b4ae9f92477052ad8529f05130ff /bin/bash")

if __name__ == "__main__":
    main()
