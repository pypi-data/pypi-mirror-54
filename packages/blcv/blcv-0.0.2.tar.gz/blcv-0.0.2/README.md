# Blender for cv
This repo provides tutorials and a library to help CV researchers to generate data using blender.

## Introduction

Blender is good for single image rendering; it provides complete python interface and good support for shapenet models.

Game engine based software (Unreal, Unity) provides a virtual world for simulation, which is better for agents to interact with the environment; a lot of VR assets to buy in the market.

## Blender tutorial

#### panel

The whole interface is divided into several panels, each panel has type and the type can be changed (3D view, Timeline, etc).

![pic1](./pics/pic1.jpg)

##### split new panel

To create more panels, drag the triangle on the right top of the main panel, and pull towards left or down, a new panel will appear.

![pic2](./pics/pic2.jpg)

##### merge panels

To merge two panels, drag the triangle and pull towards top or right to merge the corresponding panel.

![pic3](./pics/pic3.jpg)

#### Navigate

left click - pivot point

right click - select

wheel - zoom in / out

#### Import object

File -> import -> .obj

Press F12 to render the image (see the objects from camera point)

Press F11 to go back

#### Change the camera location in the interface

Directly move the camera and point light in the 3D viewpoint scene. Use the options below to change the location, rotation and scale.

![pic4](./pics/pic4.jpg)

Select the object panel and change the number of these objects.

![pic5](./pics/pic5.jpg)

Use the **view** menu to toggle to other views. (The example below shows the top view)

![pic6](./pics/pic6.jpg)

#### Add more object to the scene

From the left panel **Create** to find objects to put into the scene.

All the objects in the scene are shown in the **Outliner** panel.

![pic7](./pics/pic7.jpg)

#### Use python to control the scene

Switch the bottom panel to **python console**

Try to print `hello world`

![pic8](./pics/pic8.jpg)

But how to control objects in the scene by python?

Use the **bpy** module provided by Blender to access the scene.

Hover over text field to get the object's python value and change it in python console using python grammar.

![pic9](./pics/pic9.jpg)

#### Build the automation pipeline

Switch the panel type to **text editor**,  new or open a file and write python script in it.

![pic10](./pics/pic10.jpg)

Finish your script then click **Run script** to see the difference.

*Be aware that while writing in the file, you need to **import bpy** first, or there may be error.* 

![pic11](./pics/pic11.jpg)

## Best way to run the script

In the last section, we introduce the way of running script within Blender, but usually we would like to run it in the command line. 

This section tells how to write scripts to achieve generating images automatically.

To start Blender in the command line, we can use `blender --script xxx.py` to run `xxx.py` in Blender

#### Two types of python scripts

- Outside to call Blender
- Inside Blender to control Blender





