import psutil
import win32gui

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
    Displays the element of an enumerable (one element per line).
    '''
    for element in enum:
        print(element)

if __name__ =="__main__":
    pass
