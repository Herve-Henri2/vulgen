import subprocess
from time import sleep    


def main():
    print("Welcome !\n"
          "In the current folder you will find a binary vulnerable to a buffer overflow.\n"
          "It is up to you to exploit it succesfully.\n"
          "You will also find its source code.\n\n")
        
    input("Now press Enter to start a bash terminal.\n\n")
    
    subprocess.call([""], shell=False, executable='/bin/bash')
    
    print("\n\nYou have exited the terminal. Bye !\n")
    sleep(2)


if __name__ == '__main__':
    main()
