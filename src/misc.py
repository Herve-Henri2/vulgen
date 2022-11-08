import psutil
import os


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


def open_terminal(command=None):
    '''
    Opens up a terminal (or command prompt).
    ---------------
    Parameters:

    command: str
    The command to be executed after the terminal's openingss
    '''
    
    if not command:
        command = "exec bash -i"
    os.popen(f"gnome-terminal -- bash -c \"{command};exit; exec bash -i\"")


if __name__ =="__main__":
    pass
