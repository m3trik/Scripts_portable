-- |||||||||||||||||||||||||||||||||||||||||||||||||
-- |||				3ds max macros				||||


-- fn func=
-- (
-- 	return (python.Import "tk_slots_max_init").Init()
-- )

func = (python.Import "tk_slots_max_init").Init

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
	python.Execute "if 'tk' not in locals() or 'tk' not in globals(): import tk_max; tk = tk_max.Tk_max();" --create instance
	python.Execute "tk.hide(); tk.show();"
-- 	python.Execute "if not tk.isVisible(): tk.show()"
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
	func.toggleXraySelected()
)


macroScript toggleBackfaceCull --toggle backface culling for all geometry
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(
	func.toggleBackfaceCull()
)


macroScript toggleMaterialOverride --toggle material override in viewport
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(
	func.toggleMaterialOverride()
)


macroScript convertToPolygon
category: "tk_macroScript.edit"
silentErrors: false
autoUndoEnabled: true
(
	func.convertToEditPoly()
)


macroScript toggleSmoothPreview
category: "tk_macroScript.viewport"
silentErrors: false
autoUndoEnabled: false
(
	func.toggleSmoothPreview()
)


macroScript objectMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(

	func.setSubObjectLevel(0)
)


macroScript componentVertexMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	func.setSubObjectLevel(1)
)


macroScript componentEdgeMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	func.setSubObjectLevel(2)
)


macroScript componentFacetMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	func.setSubObjectLevel(4)
)


macroScript componentElementMode
category: "tk_macroscript.selection"
silentErrors: false
autoUndoEnabled: false
(
	func.setSubObjectLevel(5)
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


-- --  depricated: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  --
