## tk_hotBox
###### *PySide marking menu style layered ui and toolkit for maya and max.
*work in progress..*

![alt text](https://raw.githubusercontent.com/m3trik/tk_hotBox/master/docs/Screenshot-Camera_navigation.jpg)
*Example of camera navigation.



## Design:
######
*This is a cross-platform, modular, marking menu style ui based on a QStackedLayout. Each piece is constructed dynamically
to allow for as little overhead as possible in construction and maintainence. Literally all you have to do to have 
a new layout up and running, is to drop a qt designer ui file into the ui folder, create a module and class of the 
same name. Naming convention allows for a stacked ui to be constructed, signals added/removed, and a master dictionary 
(stored within the switchboard module) to be created, with built-in methods that allow getting/setting of relevant data
across modules from one easy, and reliable location.*



##
-----------------------------------------------
 Structure:
-----------------------------------------------

## tk_main: 
######
*handles main gui construction.*

* set window flags and attributes.

* add each ui to a layout stack.

* store and resize each ui.

* handle coordinates to populate ui at cursor position.

* set event filters and overrides for the main, and child widgets.

* construct an overlay for paint events.




## tk_switchboard: 
######
* get dynamic ui files relative to folder location.

* build connection dict for each class with it's corresponding signals and slots.

* construct signal connections.

*the following is an example of some of the data held for each tool class instance.*

* class name as string

* class object

* widget size

* widget type

* widget name/method name as string

* widget Object

* widget Object with Signal

* method Object

* method docString

* uiList : *string list of all ui filenames in the ui folder*

* previousName : *list of last called relevant ui*

* previousView: *index of the last valid previously opened ui name.*

* prevCommand : *history of commands. uses the method docstring to generate a user friendly name from the dynamic element and stores it along side the command method.*



## tk_slots_: 
######
*master class holding methods that are inherited across all app specific slot class modules.*




##
-----------------------------------------------
 Naming convention:
-----------------------------------------------

######
* ui files:     \<name\>.ui
 
* tools module: tk_slots_\<app\>_\<name\>.py
 


*Each ui widget looks to connect to a corresponding class method of the same name: ie. widget b021 connects to method b021. The following naming convention isn't required, but using something like it helps keep things organized.*
*The docstring of each method houses a user friendly name that is stored with all other widget info in the switchboard dict when an
instance is populated. All of the ui widgets have an event filter attached for additional handling of specific events.*

* QPushButton   b000    (b000-b999) can contain 1000 buttons of one type max per class using this convention.

* QPushButton   v000    triggered on mouse release when hovered.

* QPushButton   i000    triggered on mouse release when hovered. changes the ui index.

* QComboBox     cmb000  ""

* QCheckBox     chk000  ""

* QSpinBox      s000    ""

* QtextField    t000    ""




##
-----------------------------------------------
 Basic use:
-----------------------------------------------

######
* pressed hotkey shows instance. release hides;

* mouse not pressed: heads up info

* right mouse down: shows main navigation window.

* releasing the mouse over any of the buttons in those windows takes you to the corresponding sub-menu.

* left mouse down: shows viewport navigation and camera settings.

* middle mouse down: shows embedded app ui (ie. maya's outliner, or max's modifier stack).

* double left mouseclick: produces last used orthographic view.

* double right mouseclick: produces last sub-menu.

* double middle mouseclick: repeats last command.

* dragging on an empty area of the widget moves the window and pins it open.

* mouse over buttons while window pinned to get a tooltip explanation of its function.

* holding ctrl while using Spinboxes increments/decrements by an extra decimal.




##
-----------------------------------------------
 Installation:
-----------------------------------------------
######
(Assuming the directory structure is left intact).

In maya:
* add \maya\tk_slots_maya directory to maya.env
 (MAYA_SCRIPT_PATH=<dir>)
 
In 3ds Max
* add \max\startup directory to system path by navigating in app to:
 main menu> customize> additional startup scripts
 
The default hotkey for launching the menu set is f12. This is because I usually remap f12 to the windows key. This can be changed in the tk_main module.
