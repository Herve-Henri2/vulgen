import sys, subprocess, platform, os
operating_system = platform.system()

# if any issue, please upgrade pip by typing 'python -m pip install --upgrade pip' in a shell

if operating_system == "Windows":
    try:
        import win32gui
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])

try:
    from PyQt6.QtCore import *
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqt6'])

try:
    import docker
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'docker'])

try:
    import psutil
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])

try:
    import regex
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'regex'])

