## tk_hotBox
###### *PySide marking menu style layered ui and toolkit for maya and max.


*work in progress..*

## Design:
###### 
*To build a app agnostic modular ui to house tools where each piece is constructed dynamically to allow 
for as little overhead as possible in construction and maintainence. Literally all you have to do to have 
a new ui up and running, is to drop a qt ui file into the ui folder, and create a module and class of the 
same name. Naming convention allows for a stacked ui to be built, signals added/removed, and a master dictionary 
(stored in the switchboard module) to be created, that handles the getting/setting of all data from one 
simple location, in one simple way.*

##
-----------------------------------------------
 structure:
-----------------------------------------------

## tk_main: *handles main gui construction.*
######
get dynamic ui files relative to folder location.
handle coordinates to populate ui at cursor position.
add each ui to a layout stack.
set window flags and attributes.
set event filters and overrides.
construct paint event overlay.


## tk_signals: *constructs signal connections.*
######
build connection dict in switchboard for each class with corresponding signals and slots.
add/remove signals using the switchboard dict each time the stacked layout index is changed.



## tk_slots: *master class holding methods that are inherited across all app specific slot class modules.*



## tk_switchboard: 
######
*holds the following information for each tool class instance. From this information, you can call switchboard methods to 
get most relevent information easily wherever you need it.*

class name as string
class object 
widget size
widget name/method name as string 
widget Object
widget Object with Signal
method Object
method docString
uiList : *string list of all ui filenames in the ui folder*
prevName : *list of last called relevant ui*
prevCommand : *history of commands. uses the method docstring to generate a user friendly name from the dynamic element and stores it along side the command method.*



##
-----------------------------------------------
 naming convention:
-----------------------------------------------

######
ui files:     <name>.ui
tools module: tk_slots_<app>_<name>.py     
class name:   <Name>

*widget/corresponding class methods share the same naming convention across all modules: ie. widget b021 connects to method b021.
the docstring of each method houses a user friendly name that is stored with all other widget info in the switchboard dict when an
instance is populated. Any of the buttons will also connect to a corresponding class method should it exist.*

QPushButton   b000    (b000-b999) can contain 1000 buttons of one type max per class using this convention. 
QPushButton   v000    these buttons are attached an event filter to change the ui index.
QPushButton   i000    buttons that are initially invisible.
QComboBox     cmb000  ""
QCheckBox     chk000  ""
QSpinBox      s000    ""
QtextField    t000    ""



##
-----------------------------------------------
 basic use:
-----------------------------------------------

######
pressed hotkey shows instance. release hides;
mouse not pressed: heads up info
right mouse down: shows main navigation window.
left mouse down: shows viewport navigation.
middle mouse down: shows mesh display options.
releasing the mouse over any of the buttons in those windows takes you to the corresponding submenu.
double left mouseclick: produces last used window.
double right mouseclick: repeats last command.
dragging on an empty are of the widget moves the window and pins it open in a separate instance.
holding ctrl while using Spinboxes increments/decrements by an extra decimal place.
mouse over buttons while window pinned to get an explanation of its function.
