# File made for testing purposes.
import win32gui, win32con
import psutil
import subprocess
import json

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

def main():
    test_json()

if __name__ == "__main__":
    main()
