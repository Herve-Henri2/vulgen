import os
from docker_utils import *
from misc import *


def ClearBeforeMenu():
    print("\nPress Enter to return to the main menu.")
    input()
    os.system("clear")

def HandleUserInput(choice):
    valid_inputs = [f'{i}' for i in range(1,6)]
    
    if choice not in valid_inputs:
        error(f"Invalid input, you must enter a number in {valid_inputs}.")
    elif choice == '1':
        RunContainer()
    elif choice == '2':
        RunContainer(method = "bash")
        return
    elif choice == '3':        
        DisplayImages()
    elif choice == '4':
        DisplayContainers()
    elif choice == '5':
        print('Okay bye!\n')
        return
    
    ClearBeforeMenu()
        

def main():
    InitializeDocker()
    
    choice = -1
    
    while choice != '5':
        choice = input('------------------------------------------------\n'
                    'Vulnerable environment generator main menu\n'
                    '------------------------------------------------\n'
                    'What do you wish to do?\n'
                    '1: Run container\n'
                    '2: Access container as a bash\n'
                    '3: Display Images list\n'
                    '4: Display Containers list\n'
                    '5: Exit\n'
                    '------------------------------------------------\n'
                    'Your choice: ')
        print()
        HandleUserInput(choice)
        


if __name__ == "__main__":
    main()

