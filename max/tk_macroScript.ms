--||||||||||||||||||||||||||||||||||||||||||||||
--||||||||||      3ds max macros     |||||||||||
--!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

-- python.Import "time"
-- python.Import "sys, os.path"
-- -- python.Execute("sys.path.append(os.path.expandvars('%CLOUD%/_Programming/Qt/__path'))")
-- python.Execute("sys.path.append(os.path.expandvars('C:/Users/render/Documents/_portable/Scripts_portable/Qt/__path'))")
-- python.Execute("sys.path.append(os.path.expandvars('C:/Users/render/Documents/_portable/Scripts_portable/3dsMax/__path/tk_slots'))")

tk_main = python.Import "tk_main" --hotBox module
func = python.Import "tk_slots_max_init"
func=func.Init

--macro syntax:
--	macroScript scriptName
--	category: "CategoryName"
--	buttonText: "text"
--	toolTip: "annotation"
--	icon: #("string", index)
--	silentErrors: boolean
--	autoUndoEnabled: boolean
--	(
--		script_body
--	)

-- -----------------------------------------------




macroScript tk_main
category: "tk_macroScript.ui"
silentErrors: false
autoUndoEnabled: false
(
	python.Execute "if 'tk_hotBox_init' not in locals() or 'tk_hotBox_init' not in globals(): tk_hotBox_init = tk_main.createInstance()"
	python.Execute "if not tk_hotBox_init.isVisible(): tk_hotBox_init.show()"
)

macroScript toggleGrid
Category: "tk_macroScript.ui"
silentErrors: true
autoUndoEnabled: false
(
	max grid toggle --toggle viewport grid
	actionMan.executeAction 0 "370"  -- Tools: Viewport Selection Show Selection Bracket Toggle
)

macroScript toggleUi -- hide menuBar not working
category: "tk_macroScript.ui"
silentErrors: false
autoUndoEnabled: false
(
	state = statusPanel.visible
	if state == false 
		then
		(
-- 		(dotnetclass "Autodesk.Windows.ComponentManager").QuickAccessToolBar.IsMenuBarVisible = true --show menuBar 3rd party
		--trackviews.currenttrackview.ui.showMenuBar = true --show menuBar
	-- 	timeSlider.setVisible (true) -- show timeSlider
	-- 	trackbar.visible = true -- show trackBar
		statusPanel.visible = true -- show statusPanel
		actionMan.executeAction 0 "411" --toggle toolBar
		)
	else 
		(
-- 		(dotnetclass "Autodesk.Windows.ComponentManager").QuickAccessToolBar.IsMenuBarVisible = false --hide menuBar 3rd party
		--trackviews.currenttrackview.ui.showMenuBar = false	--hide menuBar
	-- 	timeSlider.setVisible (false) -- hide timeSlider
	-- 	trackbar.visible = false -- hide trackBar
		statusPanel.visible = false -- hide statusPanel
		actionMan.executeAction 0 "411" --toggle toolBar
		)
)

macroScript snapToGrid
category: "tk_macroScript.translate"
silentErrors: false
autoUndoEnabled: false
(
	if (snapmode.getOSnapItemActive 4 1 == false) then
	(
		func.setSnapState("false")
		snapmode.setOSnapItemActive 4 1 (true);
		snapMode.active = true;
	)
	else
	(
		snapmode.setOSnapItemActive 4 1 (false);
		snapMode.active = false;
	)

	if (snapmode.getOSnapItemActive 4 2 == false) then
	(
		snapmode.setOSnapItemActive 4 2 (true);
		snapMode.active = true;
	)
	else
	(
		snapmode.setOSnapItemActive 4 2 (false);
		snapMode.active = false;
	)
)

macroScript snapToVert
category: "tk_macroScript.translate"
silentErrors: false
autoUndoEnabled: false
(
	if (snapmode.getOSnapItemActive 7 1 == false) then
	(
		func.setSnapState("false")
		snapmode.setOSnapItemActive 7 1 (true);
		snapMode.active = true;
	)
	else
	(
		snapmode.setOSnapItemActive 7 1 (false);
		snapMode.active = false;
	)

)

macroScript snapToEdge
category: "tk_macroScript.translate"
silentErrors: false
autoUndoEnabled: false
(
	if (snapmode.getOSnapItemActive 7 3 == false) then
	(
		func.setSnapState("false")
		snapmode.setOSnapItemActive 7 3 (true);
		snapMode.active = true;
	)
	else
	(
		snapmode.setOSnapItemActive 7 3 (false);
		snapMode.active = false;
	)
)

macroScript snapToMiddleEdge
category: "tk_macroScript.translate"
silentErrors: false
autoUndoEnabled: false
(
	if (snapmode.getOSnapItemActive 7 4 == false) then
	(
		func.setSnapState("false")
		snapmode.setOSnapItemActive 7 4 (true);
		snapMode.active = true;
	)
	else
	(
		snapmode.setOSnapItemActive 7 4 (false);
		snapMode.active = false;
	)
)

macroScript toggleXraySelected --toggle xray for the selected object
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(
	if ($ != undefined) then
	(
		toggle = not $.xray;
		$.xray = toggle;
	)
)

macroScript toggleBackfaceCull --toggle backface culling for all geometry
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(
	toggle = not $.backfacecull;
	
	for obj in Geometry do
	(
		obj.backfacecull = toggle;
	)
)

macroScript convertToPolygon
category: "tk_macroScript.edit"
silentErrors: false
autoUndoEnabled: true
(
-- 	sel = func.makeSelection "Current" 0

	macros.run "Modifier Stack" "Convert_to_Poly"
	maxOps.CollapseNode obj off --collapse modifier stack
--python wrapper error
-- 	for obj in sel do
-- 	(
-- 	-- 	$.convertToPoly
-- 	macros.run "Modifier Stack" "Convert_to_Poly"
-- 	maxOps.CollapseNode obj off --collapse modifier stack
-- 	)
)

macroScript toggleSmoothPreview
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(	--framework for future function.
	state = false
	for obj in (selection as array) do
	(
		for m in obj.modifiers where --modify this to toggle 
		(classof m) == TurboSmooth do --classOf checks if m is a TurboSmooth Modifier and then disables it
		(
			m.enabled = state
		)
	)
	-- toggle Preferences\viewport\selection highlighting
)

macroScript objectMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
--documentaion on subObjectLevel
--http://docs.autodesk.com/3DSMAX/16/ENU/MAXScript-Help/index.html?url=files/GUID-BAC3CC23-9D1D-44CE-B4AF-C0CEBDD7099E.htm,topicNumber=d30e673804
(
	lvl = 0
	if (subobjectlevel != lvl or subobjectlevel == undefined) then 
	(
		subobjectlevel = lvl	--set selection type to object mode
		if ($.baseObject != undefined) then
		(
		max modify mode
		modPanel.setCurrentObject $.baseObject;
		)	
	)
)

macroScript componentVertexMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	classString = func.makeSelection "Current" 1 func.classInfo
	--	[1] --object
	--	[2] --baseObject
	-- 	[5] --baseObject class
	-- 	[7] --baseObject class type string. eg. Editable,Shape,Geometry
	if (classString[1] != "noSelection") then
	(
		lvl = 1
		if (classString[7] == "Editable_Poly" and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to vertex
		)
		lvl = 1
		if (classString[7] == "Editable_Mesh" or classString[5] == Editable_mesh and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to vertex
		)
		lvl = 1
		if (classString[7] == "Editable_Patch" or classString[5] == Editable_Patch and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to vertex
		)
		lvl = 1
		if (classString[7] == "NURBSSurf" or classString[5] == NURBSSurf and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to surface cv
		)
		lvl = 1
		if (classString[7] == "Shape" and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to vertex
		)
		if (classString[7] == "Geometry") then
		(
			print "non-deformable object: Geometry";
		)
		/*else if undefined*/
		if (classString[7] == undefined) then
		(
			if (classString[5] != NURBSSurf and classString[5] != Editable_Patch and classString[5] != Editable_mesh) then
			(
				print "non-deformable object: undefined";
			)
		)
	)
	else --default
	(
		lvl = 1
		if (subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;
		)
	)
)

macroScript componentEdgeMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	classString = func.makeSelection "Current" 1 func.classInfo
	--	[1] --object
	--	[2] --baseObject
	-- 	[5] --baseObject classW
	-- 	[7] --baseObject class type string. eg. Editable,Shape,Geometry
	if (classString[1] != "noSelection") then
	(
		lvl = 2
		if (classString[7] == "Editable_Poly" and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to border edge
		)
		lvl = 2
		if (classString[7] == "Editable_Mesh" or classString[5] == Editable_mesh and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to border edge
		)
		lvl = 2
		if (classString[7] == "Editable_Patch" or classString[5] == Editable_patch and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to handle
		)
		lvl = 2
		if (classString[7] == "NURBSSurf" or classString[5] == NURBSSurf and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to surface cv
		)
		lvl = 2
		if (classString[7] == "Shape" and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to segment
		)
		if (classString[7] == "Geometry") then
		(
			print "non-deformable object: Geometry";
		)
		/*else if undefined*/
		if (classString[7] == undefined ) then
		(
			if (classString[5] != NURBSSurf and classString[5] != Editable_Patch and classString[5] != Editable_mesh) then
			(
				print "non-deformable object: undefined";
			)
		)
	)
	else --default
	(
		if (subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;
		)
	)
)

macroScript componentAltMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	classString = func.makeSelection "Current" 1 func.classInfo
	--	[1] --object
	--	[2] --baseObject
	-- 	[5] --baseObject classW
	-- 	[7] --baseObject class type string. eg. Editable,Shape,Geometry
	if (classString[1] != "noSelection") then
	(
		lvl = 3
		if (classString[7] == "Editable_Poly" and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to border edge
		)
		lvl = 3
		if (classString[7] == "Editable_Mesh" or classString[5] == Editable_mesh and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to face
		)
		lvl = 5
		if (classString[7] == "Editable_Patch" or classString[5] == Editable_patch and subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to handle
		)
		if (classString[7] == "NURBSSurf" or classString[5] == NURBSSurf) then
		(
			print "NURBSSurf has no associated function"
		)
		if (classString[7] == "Shape") then
		(
			print "Shape object has no associated function";
		)
		if (classString[7] == "Geometry") then
		(
			print "non-deformable object: Geometry";
		)
		/*else if undefined*/
		if (classString[7] == undefined ) then
		(
			if (classString[5] != NURBSSurf and classString[5] != Editable_Patch and classString[5] != Editable_mesh) then
			(
				print "non-deformable object: undefined";
			)
		)
	)
	else --default
	(
		lvl = 3
		if (subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;
		)
	)
)

macroScript componentFacetMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	classString = func.makeSelection "Current" 1 func.classInfo
	--	[1] --object
	--	[2] --baseObject
	-- 	[5] --baseObject classW
	-- 	[7] --baseObject class type string. eg. Editable,Shape,Geometry
	if (classString[1] != "noSelection") then
	(
		lvl = 4
		if (classString[7] == "Editable_Poly") then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to polygon
		)
		lvl = 4
		if (classString[7] == "Editable_Mesh" or classString[5] == Editable_mesh) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to polygon
		)
		lvl = 3
		if (classString[7] == "Editable_Patch" or classString[5] == Editable_patch) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to patch
		)
		lvl = 2
		if (classString[7] == "NURBSSurf" or classString[5] == NURBSSurf) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to surface
		)
		lvl = 3
		if (classString[7] == "Shape") then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;	--set selection type to spline
		)
		if (classString[7] == "Geometry") then
		(
			print "non-deformable object: Geometry";
		)
		/*else if undefined*/
		if (classString[7] == undefined ) then
		(
			if (classString[5] != NURBSSurf and classString[5] != Editable_Patch and classString[5] != Editable_mesh) then
			(
				print "non-deformable object: undefined";
			)
		)
	)
	else --default
	(
		lvl = 4
		if (subobjectlevel != lvl) then
		(
			modPanel.setCurrentObject classString[2];
			subobjectlevel = lvl;
		)
	)
)






-- macroScript toggleToolbar
-- category: "tk_macroScript.ui"
-- silentErrors: false
-- autoUndoEnabled: false
-- (

-- )
















/*	macroScript Documentation


You can use non-alpha numeric characters to define any of the argument strings. This includes support for escaped double quote characters: \".



The category: argument specifies in which category in the Customize User-Interface dialog the MacroScript name will be listed. The use of categories is intended to help you organize 
your MacroScripts into groupings so that the MacroScript names are less likely to clash. If you do not specify a category, a default category of "unknown" is used.
The internalCategory argument is intended to identify operations in .cui, .mnu, and .kbd files.


The toolTip: argument specifies the tooltip for the button. If no tooltip is specified, <name> is displayed for the button.


The buttonText: argument specifies the text that will appear in the button, and the icon: argument specifies the icon that will appear in the button. You can choose in the Customize
User Interface dialog whether the buttonText or icon appears in the button. If no buttonText: argument is specified, the MacroScript name is used as the buttonText .


The icon: argument specifies the icon bitmap file and the icon image within the icon bitmap file. The icon bitmap file must be located in the current 3ds Max user-interface directory. 
Icon bitmap files have a base name, such as "MyToolbar", followed by a suffix, such as "_24i.bmp", that specifies the individual icon size and icon bitmap file type. 
The icon: argument string is just the base name, with no extensions present. This base name is the name shown in the Image Group list in the Customize User-Interface dialog.
Each icon bitmap file can have any number of individual icons, lined up side-by-side in the file. If the icon bitmap file contains multiple icons, 
<index> specifies which icon in the icon bitmap file to use. The left-most icon has an <index> of 1. 
The 3ds Max internal icons (Image Group Internal in the Customize User-Interface dialog) are not stored in an icon file, and are referenced by using an empty string as the icon: argument.

So, the icon: argument can be either a two-element array containing the icon bitmap file’s base name as a string and the icon’s index in that file, or just a base name string, 
with the index 1 assumed.

ex:
 macroScript Box category:"Objects" tooltip:"Box"
icon:#("standard", 1) -- use first icon in standard
	(
  StartObjectCreation Box
	)
 macroScript Sphere category:"Objects" tooltip:"Sphere"
icon:#("", 2) -- use second icon in internal icons
	(
  StartObjectCreation Sphere
	)
 macroScript Cone category:"Objects" tooltip:"Cone"
icon:"myicon" -- use first icon in myicon
	(
  StartObjectCreation Cone
	)
-- See Creating Icon Bitmap Files for more information.


The silentErrors: parameter gives control over whether MAXScript runtime error messages are displayed while executing the MacroScript. If this parameter is set to true , 
error messages will not be displayed. This may be useful for distributed MacroScripts that may confuse the user with MAXScript error messages. The default value is false .


The autoUndoEnabled: parameters controls whether the MacroScript body will be automatically wrapped in a theHold begin/accept calls internally.


When set to false , the execution of the MacroScript body will not generate an undo record for the whole MacroScript.


When set to true or not specified, the whole MacroScript body will create an undo record when executed.


The default value is true .


Available in 3ds Max 2010 and higher.


ex:
MacroScript MacroScript_autoUndoEnabled_test1
category:"MacroScript_autoUndoEnabled_test"
buttontext:"test1"
autoUndoEnabled:false
	(
  format "test1\n"
  format "expecting theHold.holding == false, got: %\n" (theHold.holding())
  format "expecting theHold.IsSuspended == false, got: %\n" (theHold.IsSuspended())
  format "expecting theHold.Restoring == false, got: %\n" (theHold.Restoring())
  format "expecting theHold.Redoing == false, got: %\n" (theHold.Redoing())
  format "expecting theHold.RestoreOrRedoing == false, got: %\n" (theHold.RestoreOrRedoing())
  format "expecting theHold.SuperLevel == 0, got: %\n" (theHold.SuperLevel())
	)

-- The <macro_script_body> can be one of two forms.
The body can be either a single MAXScript expression, or a set of event handlers.
An <event_handler> is a special function definition local to the macroscript that handles events generated by 3ds Max.

The valid <event_name> are:

on isChecked do <expr>   
If <expr> returns true and the macroscript item is in a menu or quad menu, a check mark is placed next to the macroscript item. 
If the macroscript is a toolbar button, the button will appear as "pressed in". The do is optional for this event handler. 
If this event handler is not specified, the item will not be checked.

on isEnabled do <expr> 
If <expr> returns false and the macroscript item is in a menu or quad menu, the macroscript item will not appear in the menu or quad menu. 
If the macroscript is a toolbar button, the button will be disabled. The do is optional for this event handler. If this event handler is not specified, the item will be enabled.

on isVisible do <expr> 
If <expr> returns false and the macroscript item is in a menu or quad menu, the macroscript item will not appear in the menu or quad menu. 
If the macroscript is a toolbar button, this handler has no affect. The do is optional for this event handler. If this event handler is not specified, the item will be visible.

on execute do <expr> 
The expression evaluated when the menu or quad menu item is chosen, or the toolbar button clicked. A runtime error will be generated if this event handler is not specified.

SCRIPT:
macroScript Free_Camera
category:"Lights and Cameras"
internalcategory:"Lights and Cameras"
tooltip:"Free Camera"
buttontext:"Free Camera"
Icon:#("Cameras",2)
	(
  on execute do StartObjectCreation FreeCamera
  on isChecked return (mcrUtils.IsCreating FreeCamera)
	)

SCRIPT:
macroScript SubObject_Vertex
buttonText:"Vertex"
category:"Modifier Stack"
internalCategory:"Modifier Stack"
tooltip:"Vertex Sub-object Mode"
icon:#("SubObjectIcons",1)
	(
  on isChecked do (subObjectLevel == 1 and filters.canSwitchTo_Vertex())
  on isEnabled do Filters.canSwitchTo_Vertex()
  on isVisible do Filters.canSwitchTo_Vertex()
  on execute do
  	(
    if subObjectLevel == undefined then max modify mode
    if subObjectLevel != 1 then subObjectLevel = 1 else subObjectLevel = 0
  	)
	)
   

on altExecute <type> do <expr> 
If a macroScript implements the altExecute event handler, then a mouse icon (with dark click button) appears in the quad menu item that corresponds to the macroScript. 
When the icon is clicked, the event handler is executed with <type> being #default .

For example, the following adds alternative execute functionality to the standard "Wire Parameters" quad menu. 
When you click the icon, it pops the Param Wiring Editor instead of putting into the Wiring mode.
SCRIPT:
macroScript paramWire
category:"Parameter Wire"
internalcategory:"Parameter Wire"
buttonText:"Wire Parameters"
tooltip:"Start Parameter Wiring"
Icon:#("MAXScript" ,1)
	(
  on isEnabled return selection.count == 1
  on execute do(paramWire.start())
  on altExecute type do
  	(
    paramWire.OpenEditor()
  	)
	)

on closeDialogs do <expr> 
The closeDialogs is handler is called instead of the on Execute handler whenever the isChecked handler returns true (the button / icon /item is checked). 
It can be used to TOGGLE back to the unchecked state. This handler should implement any cleanup code that closes any open dialogs and basically returns the macroScript 
to a pre-executed state.

NOTE:The closeDialogs handler depends on the existence of the isChecked handler. If an on closeDialogs handler is defined without an isChecked handler to be defined, 
a compile-time error will be thrown!

Here is an test of a MacroScript which toggles its rollout on and off:
SCRIPT:
macroScript testCloseDialogs category:"MXS Help"
	(
	rollout testCloseRollout "Test" --define a rollout
	(
	label lb_test "testing CloseDialogs handler..."
	)
on isChecked do testCloseRollout.open 
	--return true if rollout is open 
	--if isChecked returns false (the rollout is not open in a dialog), 
	--the on execute handler will be called and will create the dialog.

on execute do createDialog testCloseRollout

  --If isChecked returns true and the user pressed the button again, 
  --instead of calling the on execute handler, the macroScript will call 
  --the on closeDialogs handler and destroy the dialog.

on closeDialogs do destroyDialog testCloseRollout
	)

  --If you drag the macroScript to a toolbar and click the button, 
  --a dialog should appear and the button should be checked. 
  --Click it again and the dialog will disappear. 
  --Repeat as often as you want - the dialog will be toggled on and off! 
   
on droppable <window> node:point:do... 
   

on drop <window> node:point:do... 
These optional MacroScript event handlers can be used to define so-called DropScripts that can be used in conjunction with the i-Drop technology. See DropScript Events for details.

The <macro_script_body> can contain global and local variables, functions, and structure definitions. The <macro_script_body> is compiled in its own local scope, and the locals are only 
visible inside the scope of the MacroScript. MacroScript locals are heap-based locals, which are slightly different from normal (stack-based) locals.
Normal locals are visible in the current scope and have a lifetime of one execution of that scope. Heap-based locals are also visible only in the current scope, but have a lifetime equal 
to the lifetime of the top-level expression where they are defined. A MacroScript’s locals are created the first time you execute the MacroScript, initialized to a value of undefined , 
or to their specified initialization value. These values are stored in a separate memory stack. On entry to each function (or top level script) in the MacroScript, a ’r;frame’ in the 
memory stack is marked and when the function (or top level script) exits, all of the values in the frame are freed from the memory.
Because a MacroScript’s name is not created as a variable, you cannot access a MacroScript’s locals outside the scope of the MacroScript. So, for example, you can create a rollout in a 
MacroScript, and the rollout’s event handlers can access the locals defined in the MacroScript because the rollout is executing within the scope of the MacroScript. However, you cannot 
access the MacroScript’s locals from another utility or from the Listener, because they are not executing within the scope of the MacroScript. See Scope of Variables for more information.
When you execute a macroScript definition, the return value is an integer MacroScript ID value. MAXScript internally stores information about each MacroScript in an array, and the 
returned MacroScript ID value is the array index for that MacroScript. The information stored for each MacroScript consists of the file in which that MacroScript is defined and a pointer 
into that file specifying where the MacroScript definition begins. The MacroScript definition is only compiled when you first press a toolbar button that contains the script, or execute 
the MacroScript using the macros.run() method.

*/



--deprecated
-- fn filterSelectionByBaseClass baseObjectClass=
-- 	for obj in selection do 
-- 	(
-- 		obj = classOf(obj.baseObject) --get the base object class.  ie. Editable_Poly

-- 		--Editable Mesh
-- 		if (obj == Editable_Poly) then
-- 		(
-- 			return "Editable_Poly";
-- 		)
		
-- 		--Shapes
-- 		if (obj == Line or \
-- 			obj == Circle or \
-- 			obj == Arc or \
-- 			obj == NGon or \
-- 			obj == Text or \
-- 			obj == Egg or \
-- 			obj == Rectangle or \
-- 			obj == Ellipse or \
-- 			obj == Donut or \
-- 			obj == Star or \
-- 			obj == Helix or \
-- 			obj == Section) then
-- 		(
-- 			return "Shape";
-- 		)
		
-- 		--Geometry
-- 		if (obj == Box or \
-- 			obj == Sphere or \
-- 			obj == Cylinder or \
-- 			obj == Torus or \
-- 			obj == Teapot or \
-- 			obj == TextPlus or \
-- 			obj == Cone or \
-- 			obj == GeoSphere or \
-- 			obj == Tube or \
-- 			obj == Pyramid or \
-- 			obj == Plane) then
-- 		(
-- 			return "Geometry";
-- 		)
		
-- 	)

-- --uses imported function
-- fn func.classInfo argObjects=
-- (
-- 	for obj in argObjects do
-- 	(
--     func = python.Import "func"
--     func = func.filterSelectionByBaseClass
--     baseObj = obj.baseObject
	
--     baseObjClass = classOf(baseObj) /*get the base object class.  ie. Editable_Poly*/
--     classTypeString = func(baseObjClass) /*func takes the base object class and returns the type as a string*/
-- 		superClass = superClassOf obj
-- 		isValid = isValidNode obj
		
-- 		case (superClass) of
-- 		(
-- 			GeometryClass: superClassString = "GeometryClass"
-- 			shape: superClassString = "shape"
-- 			light: superClassString = "light"
-- 			camera: superClassString = "camera"
-- 			SpacewarpObject: superClassString = "SpacewarpObject"
-- 			helper: superClassString = "helper"
-- 			system: superClassString = "system"
-- 			default: superClassString = "default" /*aka unknown type*/
-- 		)

-- 		case (baseObjClass) of
-- 		(
-- 			Box:  baseObjClassString = "Box"
-- 			Sphere:  baseObjClassString = "Sphere"
-- 			Cylinder:  baseObjClassString = "Cylinder"
-- 			Torus:  baseObjClassString = "Torus"
-- 			Teapot:  baseObjClassString = "Teapot"
-- 			TextPlus:  baseObjClassString = "TextPlus"
-- 			Cone:  baseObjClassString = "Cone"
-- 			GeoSphere:  baseObjClassString = "GeoSphere"
-- 			Tube:  baseObjClassString = "Tube"
-- 			Pyramid:  baseObjClassString = "Pyramid"
-- 			Plane:  baseObjClassString = "Plane"
-- 			Line:  baseObjClassString = "Line"
-- 			Circle:  baseObjClassString = "Circle"
-- 			Arc:  baseObjClassString = "Arc"
-- 			NGon:  baseObjClassString = "NGon"
-- 			Text:  baseObjClassString = "Text"
-- 			Egg:  baseObjClassString = "Egg"
-- 			Rectangle:  baseObjClassString = "Rectangle"
-- 			Ellipse:  baseObjClassString = "Line"
-- 			Donut:  baseObjClassString = "Donut"
-- 			Star:  baseObjClassString = "Star"
-- 			Helix:  baseObjClassString = "Helix"
-- 			Section:  baseObjClassString = "Section"
-- -- 			:  baseObjClassString = ""
-- 		)
		
-- 	    returnedClassInfoArray = #()
-- 	    append returnedClassInfoArray obj
-- 	    append returnedClassInfoArray superClass
-- 	    append returnedClassInfoArray superClassString
-- 			append returnedClassInfoArray baseObjClass
-- 	    append returnedClassInfoArray baseObjClassString
-- 			append returnedClassInfoArray classTypeString
		
-- -- 			print returnedClassInfoArray[1] --object
-- -- 			print returnedClassInfoArray[2] --superClass
-- -- 			print returnedClassInfoArray[3] --superClass returned as a string value
-- -- 			print returnedClassInfoArray[4] --baseObject class
-- -- 			print returnedClassInfoArray[5] --baseObject class returned as a string value
-- -- 			print returnedClassInfoArray[6] --baseObject class type returned as a string. eg. Editable,Shape,Geometry
-- --			print returnedClassInfoArray[7] --query is valid node --boolean 

-- 	    return returnedClassInfoArray
-- 	)
-- )


-- fn func.setSnapState state=
-- (
-- 	--set 'grid and snap settings'
-- 	--body shapes
-- 	snapmode.setOSnapItemActive 1 1 (state);
-- 	snapmode.setOSnapItemActive 1 2 (state);
-- 	snapmode.setOSnapItemActive 1 3 (state);
-- 	snapmode.setOSnapItemActive 1 4 (state);
-- 	snapmode.setOSnapItemActive 1 5 (state);
-- 	--nurbs	
-- 	snapmode.setOSnapItemActive 2 1 (state);
-- 	snapmode.setOSnapItemActive 2 2 (state);
-- 	snapmode.setOSnapItemActive 2 3 (state);
-- 	snapmode.setOSnapItemActive 2 4 (state);
-- 	snapmode.setOSnapItemActive 2 5 (state);
-- 	snapmode.setOSnapItemActive 2 6 (state);
-- 	snapmode.setOSnapItemActive 2 7 (state);
-- 	snapmode.setOSnapItemActive 2 8 (state);
-- 	snapmode.setOSnapItemActive 2 9 (state);
-- 	snapmode.setOSnapItemActive 2 10 (state);
-- 	--Point Cloud Shapes
-- 	snapmode.setOSnapItemActive 3 1 (state);
-- 	--standard
-- 	snapmode.setOSnapItemActive 4 1 (state);
-- 	snapmode.setOSnapItemActive 4 2 (state);
-- 	--standard
-- 	snapmode.setOSnapItemActive 5 1 (state);
-- 	snapmode.setOSnapItemActive 5 2 (state);
-- 	--standard
-- 	snapmode.setOSnapItemActive 6 1 (state);
-- 	snapmode.setOSnapItemActive 6 2 (state);
-- 	--standard
-- 	snapmode.setOSnapItemActive 7 1 (state);
-- 	snapmode.setOSnapItemActive 7 2 (state);
-- 	snapmode.setOSnapItemActive 7 3 (state);
-- 	snapmode.setOSnapItemActive 7 4 (state);
-- 	snapmode.setOSnapItemActive 7 5 (state);
-- 	snapmode.setOSnapItemActive 7 6 (state);
-- )
