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
4) Managing Scenarios
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
<br><br>Once you have docker up and running on your system, you can install all the librairies by running the [install_requirements.py](src/install_requirements.py) file. Make sure you have updated your pip beforehand.

    python -m pip install --upgrade pip

## 3) Using the program
To launch the program, run the [main_window.py](src/main_window.py) file.<br>
![main_window_img](https://i.imgur.com/HmiYOeT.png)<br>
The program automatically starts docker or Docker Desktop if necessary before showing the window. If you are running it on a Windows machine, it will try to locate Docker Desktop based on its default installation path. If you have it installed in another path, you will need to set it through the options window.<br>
![options_window_img](https://i.imgur.com/7XLWSOV.png)<br>
You may also change the theme, mode, and turn the auto attach feature on/off. The mode is either Education or Challenge. In Education mode, you will be able to view the scenario's attack solution after launching it, which will not be the case in Challenge mode. The auto attach feature will automatically attach a specific container to a terminal shell if it has the "requires_it" (requires interaction) attribute set to True. It is recommended that you leave that option enabled.<br>
Note that <b>you need to restart the application</b> to apply the changes.<br><br>

To Launch a scenario, first click on the Scenarios Button, select the scenario you want to launch and then simply click on the Launch Scenario button.
![launch_scenario_img](https://i.imgur.com/uUe5Ovm.png)
![active_scenario_img](https://i.imgur.com/KYkljYX.png)<br>
Adding, editing and removing scenarios will be covered in the next section.<br><br>

Although this program was not created for the following purpose, you may also manage docker images, containers and networks with it.
![manage_images_img](https://i.imgur.com/Pl66ic9.png)

## 4) Managing Scenarios

Please refer to the [MANAGE_SCENARIOS.md](Scenarios/MANAGE_SCENARIOS.md) file.

## 5) Developer Guide

Please refer to the [DEV_GUIDE.md](DEV_GUIDE.md) file.