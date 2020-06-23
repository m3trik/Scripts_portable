###### *PySide marking menu style layered ui and toolkit for maya and max.
*work in progress..*

## Design:
######
*This is a cross-platform, modular, marking menu style ui based on a QStackedWidget.  Each piece is constructed dynamically
to allow for as little overhead as possible in development and maintainence.  Naming convention and directory structure allows for a stacked ui to be constructed, signals added/removed as needed, and a master dictionary (stored within the switchboard module) to be created, which provides convenience methods that allow getting/setting of relevant data across modules.*


![alt text](https://raw.githubusercontent.com/m3trik/tk/master/docs/toolkit_demo.gif)
*Example re-opening the last scene, renaming a material, and selecting geometry by that material.


##
-----------------------------------------------
 Structure:
-----------------------------------------------

#### tk_:
###### *handles main gui construction.*

#### tk_childEvents:
###### *event handling for child widgets.*

#### tk_overlay:
###### *tracks cursor position and ui hierarchy to generate paint events that overlay the main widget.*

#### tk_switchboard:
###### *contains a master dictionary for widget related info as well as convienience classes for interacting with the dict.*

#### tk_slots_:
###### *parent class holding methods that are inherited across all app specific slot class modules.*


![alt text](https://raw.githubusercontent.com/m3trik/tk/master/docs/dependancy_graph.jpg)


##
-----------------------------------------------
 Naming convention:
-----------------------------------------------

######
*Each ui file has a corresponding slot module containing the same name that it will look to construct it's connections:
* ui file:     \<name\>.ui

* corresponding class: tk_slots_\<app\>_\<name\>.py
 

*Each ui widget looks to connect to a corresponding class method of the same name: ie. widget b021 connects to method b021. The following naming convention isn't explicitly required, but generally used throughout the code when handling widgets.*

* QPushButton             b000    (b000-b999)
* QPushButton             v000    triggered on mouse release when hovered.
* QPushButton             i000    triggered on mouse enter. changes the ui index.
* QToolButton             tb000   ""
* QComboBox               cmb000  ""
* QCheckBox|QRadioButton|QPushButton(checkable) chk000  ""
* QSpinBox|QDoubleSpinBox s000    ""
* QLabel                  lbl000  ""
* QWidget                 w000    ""
* QTreeWidget             tree000 ""
* QListWidget             list000 ""
* QLineEdit               line000 ""
* QTextEdit               text000 ""

##
-----------------------------------------------
 Basic use:
-----------------------------------------------

######
* pressed hotkey shows instance. release hides;

* mouse not pressed: heads up info

* right mouse down: shows main navigation window.

* releasing the mouse over any of the buttons in those windows takes you to the corresponding sub-menu.

* left mouse down: shows camera navigation and settings.

* middle mouse down: shows embedded app ui (ie. maya's outliner, or max's modifier stack).

* double right mouseclick: produces last used orthographic view.

* double middle mouseclick: produces last sub-menu.

* double left mouseclick: repeats last command.

* dragging the area at the top of the widget moves the window and pins it open.

* mouse over buttons while window pinned to get a tooltip explanation of its function.

* holding ctrl while using Spinboxes increments/decrements by an extra decimal.

* right clicking widgets will bring up their context menu if it exists.


##
-----------------------------------------------
 Installation:
-----------------------------------------------
######
(Assuming the default windows directory structure).

In maya:
* add \maya\tk_slots_maya directory to maya.env
 (MAYA_SCRIPT_PATH=<dir>)
 
In 3ds Max:
* add \max\startup directory to system path by navigating in app to:
 main menu> customize> additional startup scripts

Adding additional ui's:
* Drop the qt designer ui file into the ui folder.
* Add a shortcut somewhere in the main ui (with the ui name in the 'whats this' attribute).
* Create corresponding class of the same name following the naming convention and inheritance of existing slot modules.  

The default hotkey for launching the menu set is f12. This is because I usually remap f12 to the windows key. This can be changed in the tk_ module.
