import subprocess
from time import sleep


def PythonBash():
    '''
    Allows the user to interact with this script as he would with a bash terminal.
    '''    
    cmd = input("> ")
    
    sleep(1)
    
    while(cmd.lower() != "exit"):
        subprocess.call(cmd, shell=False, executable='/bin/bash')
        print()        
        cmd = input("> ")
        


def main():
    print("Hello !")
    print("This is only a test.\n")
    
    age = input("Please input your age : ")
    
    if age == '25':
        print("\nNice !\n")
    else:
        print("\nYou are " + age + " years old.\n")
        
    input("Press Enter to see this Python script.\n")
    
    subprocess.Popen(["cat", "test.py"], shell=False)
    
    sleep(2)
    
    print("\nYou will now be able to work in a terminal.\n")
    
    #PythonBash()
    subprocess.call([""], shell=False, executable='/bin/bash')
    
    print("\nYou have exited the terminal. Bye !\n")
    sleep(2)


if __name__ == '__main__':
    main()
