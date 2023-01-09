# Vulgen

### Contributors
- Hervé-Henri HOUZARD 
- Clarence GOMBAULT
- Kinan ZEIDAN 
- Matthieu LACROIX
- Léa DELMAERE
### Project Owner
- Jean-Pierre BRUANDET
#
## Summary
1) About this project
2) Installing the requirements
3) Using the program
4) Adding a scenario
5) Developer guide
#
## 1) About this project

The goal of this project is to generate vulnerable environments with the help of docker containers for cultural and educational purposes. It is meant to be a pentesting tool.
<br>Using docker containers instead of virtual machines has the advantage of alleviating the user experience, as virtual machines are often heavy, difficult to set up and unstable. If you are interested in using a pentesting program generating unsecure VMs, we invite you to check out the [SecGen](https://github.com/cliffe/SecGen) project.
<br>However, docker containers have their own limits. For example many vulnerabilities rely within the operating system's kernel, which docker does not emulate, unlike virtual machines, leaving us unable to perform training on such vulnerabilities. 
<br><br>Note that the program and default scenarios were created by students, not cybersecurity/pentesting experts. The project aims at being rookie and beginner friendly, but also help veterans to add more complex scenarios and continue this program's development. (This is what sections 4 and 5 are all about)

## 2) Installing the requirements

This program was designed so you can run it on both Linux and Windows machines. Prior to everything, you need to install a version of python >= 3.9 as well as docker on your system.
<br>Install python from [here](https://www.python.org/downloads/). 
<br>To install docker on Ubuntu, please follow this [guide](https://docs.docker.com/engine/install/ubuntu/).
<br>To install docker on Windows, you will need the [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) application.
<br><br>Once you have docker up and running on your system, you can install all the librairies by running the [install_requirements.py](src/install_requirements.py) file. Make sure you have updated your pip before hand.

    python -m pip install --upgrade pip

## 3) Using the program
To launch the program, run the [main_window.py](src/main_window.py) file. (insert image here) The program automatically starts docker or Docker Desktop if necessary before showing the window. If you are running it on a Windows machine, it will try to locate Docker Desktop based on its default installation path. If you have it installed in another path, you will need to set it through the options window. (insert image here)
