# Summary

1. Adding a Scenario
2. Editing a Scenario
3. Removing a Scenario

#
## 1) Adding a scenario

To add a scenario, click on the Add Scenario button.<br>
![add_scenario_img](https://i.imgur.com/EhDrYrp.png)
From there, you can fill in all the fields you want (or not). A scenario must have at a name as well as at least one container.<br>
![add_scenario_img2](https://i.imgur.com/pwSbcff.png)<br>
First off, when adding a container, you have to choose between the Image and DockerFile options. By ticking the image check box, you can either write down the name of the image you want to directly download, or browse through the non custom images you have downloaded and use one of those.<br>
![add_scenario_img3](https://i.imgur.com/I5vKZww.png)<br>
If you would like to build your image from scratch through the help of a DockerFile, start by creating a folder in /docker_images/scenario_images/ and name it <<span style="font-style: italic">your_scenario_name-image_name</span>>
Place your dockerfile directly inside of that folder. You may also create an empty req.txt or include a pre-built base image like kalilinux for example by writing "Image:kalilinux" inside of it (these images are in the docker_images/base_images folder).<br>
![add_scenario_img4](https://i.imgur.com/QqfSkSX.png)<br>
Once you have set up your folder and Dockerfile properly, tick the DockerFile check box, click on the Browse button and select the appropriate folder.<br>
You can define the container as the main one, and confirm whether it needs user interaction or not, in which case it may automatically attach to a terminal and open up once the scenario is launched.<br>
Note that if your scenario only has one container, it will always be set as the main one automatically.<br>
![add_scenario_img5](https://i.imgur.com/ekTk8YG.png)<br>
You can also define which networks it belongs to. By default, it will belong to the bridge network, but you can add a custom network or make it networkless as well (deselect the bridge network in order to do that).<br>
![add_scenario_img6](https://i.imgur.com/bDC5OQL.png)<br>
Finally, you can type in a container name (different from the container's image name), set the ports that you want and specify which operating system the image will be running on (for documentation purposes.) It is now ready to be saved.<br>
![add_scenario_img7](https://i.imgur.com/VObLkpd.png)<br>
Once done with all your containers and other scenario parameters, you can simply click on the Save button and it will now appear in your scenario list.

#
## 2) Editing a Scenario

To edit a scenario, simply select the one you wish to change and click on the Edit Scenario button. You then have the option to change its parameters from the windows shown above or directly open its json and README files, we do not recommend doing that though.<br>
![edit_scenario_img](https://i.imgur.com/PLPmojU.png)<br>

#
## 3) Removing a Scenario

To remove a scenario, simply select it then click on "Remove Scenario" then confirm.<br>
![remove_scenario_img](https://i.imgur.com/5AUx2jH.png)