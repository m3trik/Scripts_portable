## tk_hotBox
###### *PySide marking menu style layered ui and toolkit for maya and max.


![alt text](https://raw.githubusercontent.com/m3trik/tk_hotBox/master/docs/Screenshot-Camera_navigation.jpg)
*Example of camera navigation.

![alt text](https://raw.githubusercontent.com/m3trik/tk_hotBox/master/docs/Screenshot-Menu.jpg)
*Menu set.


## Design:
######
*This is a cross-platform, app agnostic, modular, marking menu style ui to house user tools. Each piece is constructed dynamically
to allow for as little overhead as possible in construction and maintainence. Literally all you have to do to have 
a new ui up and running, is to drop a qt designer ui file into the ui folder, create a module and class of the 
same name. Naming convention allows for a stacked ui to be built, signals added/removed, and a master dictionary 
(stored within the switchboard module) to be created that allows getting/setting of relevant data across modules from one 
easy, and reliable location.*

*continual work in progress..*

##
-----------------------------------------------
 Structure:
-----------------------------------------------

## tk_main: 
######
*handles main gui construction.*

* get dynamic ui files relative to folder location.

* handle coordinates to populate ui at cursor position.

* add each ui to a layout stack.

* set window flags and attributes.

* set event filters and overrides.

* construct paint events.


## tk_signals: 
######
*constructs signal connections.*

* build connection dict in switchboard for each class with corresponding signals and slots.

* add/remove signals using the switchboard dict each time the stacked layout index is changed.



## tk_slots: 
######
*master class holding methods that are inherited across all app specific slot class modules.*



## tk_switchboard: 
######
*the following is an example of some of the imformation held for each tool class instance. From this information, you can call switchboard methods to 
get most relevent information easily wherever you need it.*
*for a full up-to-date list, check the tk_switchboard module's docstring.*

* class name as string

* class object

* widget size

* widget name/method name as string

* widget Object

* widget Object with Signal

* method Object

* method docString

* uiList : *string list of all ui filenames in the ui folder*

* previousName : *list of last called relevant ui*

* previousView: *index of the last valid previously opened ui name.*

* prevCommand : *history of commands. uses the method docstring to generate a user friendly name from the dynamic element and stores it along side the command method.*



##
-----------------------------------------------
 Naming convention:
-----------------------------------------------

######
* ui files:     \<name\>.ui
 
* tools module: tk_slots_\<app\>_\<name\>.py
 
* class name:   \<Name\>

*widget/corresponding class methods share the same naming convention across all modules: ie. widget b021 connects to method b021.
the docstring of each method houses a user friendly name that is stored with all other widget info in the switchboard dict when an
instance is populated. Any of the buttons will also connect to a corresponding class method should it exist.*

* QPushButton   b000    (b000-b999) can contain 1000 buttons of one type max per class using this convention.

* QPushButton   i000    these buttons are attached an event filter to change the ui index.

* QComboBox     cmb000  ""

* QCheckBox     chk000  ""

* QSpinBox      s000    ""

* QtextField    t000    ""

any additional widget types can be easily added when needed using this same convention.


##
-----------------------------------------------
 Basic use:
-----------------------------------------------

######
* pressed hotkey shows instance. release hides;

* mouse not pressed: heads up info

* right mouse down: shows main navigation window.

* left mouse down: shows viewport navigation and camera settings.

* middle mouse down: shows mesh display options.

* releasing the mouse over any of the buttons in those windows takes you to the corresponding sub-menu.

* double left mouseclick: produces last used orthographic view.

* double right mouseclick: produces last sub-menu.

* double middle mouseclick: repeats last command.

* dragging on an empty area of the widget moves the window and pins it open.

* holding ctrl while using Spinboxes increments/decrements by an extra decimal place.

* mouse over buttons while window pinned to get an explanation of its function.



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
