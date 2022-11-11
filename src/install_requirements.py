import sys, subprocess, platform
operating_system = platform.system()

try:
    from PyQt6.QtCore import *
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqt6'])

try:
    import docker
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'docker'])

if operating_system == "Windows":
    try:
        import curses
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'windows-curses'])
    try:
        import win32gui
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])

elif operating_system == "Linux":
    try:
        import curses
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'curses'])