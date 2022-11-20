import subprocess
from time import sleep        


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
    subprocess.call([""], shell=False, executable='/bin/bash')
    
    print("\nYou have exited the terminal. Bye !\n")
    sleep(2)


if __name__ == '__main__':
    main()
