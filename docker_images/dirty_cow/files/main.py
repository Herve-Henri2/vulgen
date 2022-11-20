import subprocess
from time import sleep    


def main():
    print("Welcome !\n"
          "This environment is vulnerable to the dirty cow vulnerability.\n"
          "It is up to you to exploit it succesfully.\n"
          "You will find a file with a POC of the exploit in the folder of this script.\n\n")
        
    input("Now press Enter to start a bash terminal.\n\n")
    
    subprocess.call([""], shell=False, executable='/bin/bash')
    
    print("\n\nYou have exited the terminal. Bye !\n")
    sleep(2)


if __name__ == '__main__':
    main()
