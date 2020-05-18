from __future__ import print_function
import pymel.core as pm
import maya.mel as mel






class Macros(object):
	'''
	Custom scripts with assigned hotkeys.
	'''
	def __init__(self):
		'''
		'''


	def setMacros(self):
		'''
		Call setMacro for each item.
		'''
		self.setMacro('hk_back_face_culling', k='1', cat='Display', ann='Toggle back-face culling')
		self.setMacro('hk_smooth_preview', k='2', cat='Display', ann='Toggle smooth mesh preview')
		self.setMacro('hk_isolate_selected', k='F2', cat='Display', ann='Isolate current selection')
		self.setMacro('hk_grid_and_image_planes', k='F1', cat='Display', ann='Toggle grid and image plane visibility')
		self.setMacro('hk_frame_selected', k='f', cat='Display', ann='Frame selected by a set amount')
		self.setMacro('hk_wireframe_on_shaded', k='3', cat='Display', ann='Toggle wireframe on shaded')
		self.setMacro('hk_xray', k='F3', cat='Display', ann='Toggle xRay all')
		self.setMacro('hk_wireframe', k='5', cat='Display', ann='Toggle wireframe/shaded/shaded w/texture display')
		self.setMacro('hk_shading', k='6', cat='Display', ann='Toggle viewport shading')
		self.setMacro('hk_selection_mode', k='sht+q', cat='Edit', ann='Toggle between object selection & last component selection')
		self.setMacro('hk_paste_and_rename', k='ctl+v', cat='Edit', ann='Paste and rename removing keyword "paste"')
		self.setMacro('hk_multi_component', k='F5', cat='Edit', ann='Multi-Component Selection')
		self.setMacro('hk_toggle_component_mask', k='F4', cat='Edit', ann='Toggle Component Selection Mask')
		self.setMacro('hk_tk_show', k='F12', cat='UI', ann='Display tk marking menu')
		self.setMacro('hk_hotbox_full', k='sht+z', cat='UI', ann='Display the full version of the hotbox')
		self.setMacro('hk_toggle_panels', k='9', cat='UI', ann='Toggle UI toolbars')


	def setMacro(self, name=None, k=None, cat=None, ann=None):
		'''
		Sets a default runtime command with a keyboard shotcut.
		args:
			name (str) = The command name you provide must be unique. The name itself must begin with an alphabetic character or underscore followed by alphanumeric characters or underscores.
			cat (str) = catagory - Category for the command.
			ann (str) = annotation - Description of the command.
			k (str) = keyShortcut - Specify what key is being set.
						key modifier values are set by adding a '+' between chars. ie. 'sht+z'.
						modifiers:
							alt, ctl, sht
						additional valid keywords are:
							Up, Down, Right, Left,
							Home, End, Page_Up, Page_Down, Insert
							Return, Space
							F1 to F12
							Tab (Will only work when modifiers are specified)
							Delete, Backspace (Will only work when modifiers are specified)
		'''
		command = self.formatSource(name, removeTabs=2)

		#set runTimeCommand
		pm.runTimeCommand(
				name,
				annotation=ann,
				category=cat,
				command=command,
				default=True,
		)

		#set command
		nameCommand = pm.nameCommand(
				'{0}Command'.format(name),
				annotation=ann,
				command=name,
		)

		#set hotkey
		#modifiers
		ctl=False; alt=False; sht=False
		for char in k.split('+'):
			if char=='ctl':
				ctl = True
			elif char=='alt':
				alt = True
			elif char=='sht':
				sht = True
			else:
				key = char

		# print(name, char, ctl, alt, sht)
		pm.hotkey(keyShortcut=key, name=nameCommand, ctl=ctl, alt=alt, sht=sht) #set only the key press.


	def formatSource(self, cmd, removeTabs=0):
		'''
		Return the text of the source code for an object.
		The source code is returned as a single string.
		Removes lines containing '@' or 'def ' ie. @staticmethod.
		args:
			cmd = module, class, method, function, traceback, frame, or code object.
			removeTabs (int) = remove x instances of '\t' from each line.
		returns:
			A Multi-line string.
		'''
		from inspect import getsource
		source = getsource(getattr(Macros, cmd))

		l = [s.replace('\t', '', removeTabs) for s in source.split('\n') if s and not '@' in s and not 'def ' in s]
		return '\n'.join(l)



	# Display --------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def setWireframeOnShadedOption(editor, state):
		'''
		Set Wireframe On Shaded.
		args:
			editor (str) = The panel name.
			state (bool) = The desired on or off state.
		'''
		modeIsShaded = pm.modelEditor(editor, query=True, displayAppearance=True) #True if "smoothShaded", "flatShaded".

		if state and not modeIsShaded:
			pm.modelEditor(editor, edit=True, displayAppearance='smoothShaded', activeOnly=False, wireframeOnShaded=1)
		else:
			pm.modelEditor(editor, edit=True, wireframeOnShaded=0)



	@staticmethod
	def hk_back_face_culling():
		'''
		hk_back_face_culling
		Toggle Back-Face Culling
		'''
		sel = pm.ls(selection=True)
		if sel:
			currentPanel = pm.getPanel(withFocus=True)
			state = pm.polyOptions(sel, query=True, wireBackCulling=True)[0]

			if not state:
				pm.polyOptions(sel, gl=True, wireBackCulling=True)
				Macros.setWireframeOnShadedOption(currentPanel, 0)
				pm.inViewMessage(statusMessage="Back-Face Culling is now <hl>OFF</hl>.\\n<hl>1</hl>", pos='topCenter', fade=True)
			else:
				pm.polyOptions(sel, gl=True, backCulling=True)
				Macros.setWireframeOnShadedOption(currentPanel, 1)
				pm.inViewMessage(statusMessage="Back-Face Culling is now <hl>ON</hl>.\\n<hl>1</hl>", pos='topCenter', fade=True)
		else:
			print("# Warning: Nothing selected. #")



	@staticmethod
	def hk_smooth_preview():
		'''
		hk_smooth_preview
		Toggle smooth mesh preview
		'''
		selection=pm.ls(selection=1)
		scene=pm.ls(geometry=1)
		#if no object selected smooth all geometry
		if len(selection) == 0:
			for object in scene:
				if pm.getAttr(str(object) + ".displaySmoothMesh") != 2:
					pm.setAttr((str(object) + ".displaySmoothMesh"), 2)
					#smooth preview on
					pm.displayPref(wireframeOnShadedActive="none")
					#selection wireframe off
					pm.inViewMessage(position='topCenter', fade=1, statusMessage="S-Div Preview is now <hl>ON</hl>.\n<hl>2</hl>")
					
				
				else:
					pm.setAttr((str(object) + ".displaySmoothMesh"), 0)
					#smooth preview off
					pm.displayPref(wireframeOnShadedActive="full")
					#selection wireframe on
					pm.inViewMessage(position='topCenter', fade=1, statusMessage="S-Div Preview is now <hl>OFF</hl>.\n<hl>2</hl>")
					
				if pm.getAttr(str(object) + ".smoothLevel") != 1:
					pm.setAttr((str(object) + ".smoothLevel"), 1)
					
				
			
		#smooth selection only
		for object in selection:
			if pm.getAttr(str(object) + ".displaySmoothMesh") != 2:
				pm.setAttr((str(object) + ".displaySmoothMesh"), 2)
				#smooth preview on
				pm.displayPref(wireframeOnShadedActive="none")
				#selection wireframe off
				pm.inViewMessage(position='topCenter', fade=1, statusMessage="S-Div Preview is now <hl>ON</hl>.\n<hl>2</hl>")
				
			
			else:
				pm.setAttr((str(object) + ".displaySmoothMesh"), 0)
				#smooth preview off
				pm.displayPref(wireframeOnShadedActive="full")
				#selection wireframe on
				pm.inViewMessage(position='topCenter', fade=1, statusMessage="S-Div Preview is now <hl>OFF</hl>.\n<hl>2</hl>")
				
			if pm.getAttr(str(object) + ".smoothLevel") != 1:
				pm.setAttr((str(object) + ".smoothLevel"), 1)



	@staticmethod
	def hk_isolate_selected():
		'''
		hk_isolate_selected
		Isolate current selection
		Isolate selected
		'''
		currentPanel = pm.getPanel(withFocus=1)
		state = pm.isolateSelect(currentPanel, query=1, state=1)
		if state:
			pm.isolateSelect(currentPanel, state=0)
			pm.isolateSelect(currentPanel, removeSelected=1)
		else:
			pm.isolateSelect(currentPanel, state=1)
			pm.isolateSelect(currentPanel, addSelected=1)



	@staticmethod
	def hk_grid_and_image_planes():
		'''
		hk_grid_and_image_planes
		Toggle grid and image plane visibility
		'''
		image_plane = pm.ls(exactType='imagePlane')

		for obj in image_plane:
			attr = obj+'.displayMode'
			if not pm.getAttr(attr)==2:
				pm.setAttr(attr, 2)
				pm.grid(toggle=1)
				pm.inViewMessage(statusMessage="Grid is now <hl>ON</hl>.\\n<hl>F1</hl>", pos='topCenter', fade=True)
			else:
				pm.setAttr(attr, 0)
				pm.grid(toggle=0)
				pm.inViewMessage(statusMessage="Grid is now <hl>OFF</hl>.\\n<hl>F1</hl>", pos='topCenter', fade=True)



	@staticmethod
	def hk_frame_selected():
		'''
		hk_frame_selected
		Frame selected by a set amount
		'''
		pm.melGlobals.initVar('int', 'tk_toggleFrame')
		selection = pm.ls(selection=1)
		mode = pm.selectMode(query=1, component=1)
		maskVertex = pm.selectType(query=1, vertex=1)
		maskEdge = pm.selectType(query=1, edge=1)
		maskFacet = pm.selectType(facet=1, query=1)
		if len(selection) == 0:
			pm.viewFit(allObjects=1)
			
		if mode == 1 and maskVertex == 1 and len(selection) != 0:
			if len(selection)>1:
				if not pm.melGlobals['tk_toggleFrame'] == 1:
					pm.viewFit(fitFactor=.65)
					pm.melGlobals['tk_toggleFrame']=1
					print("frame vertices " + str(pm.melGlobals['tk_toggleFrame']) + "\n")

				else:
					pm.viewFit(fitFactor=.10)
					#viewSet -previousView;
					pm.melGlobals['tk_toggleFrame']=0
					print("frame vertices " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
			elif not pm.melGlobals['tk_toggleFrame'] == 1:
				pm.viewFit(fitFactor=.15)
				pm.melGlobals['tk_toggleFrame']=1
				print("frame vertex " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
			else:
				pm.viewFit(fitFactor=.01)
				#viewSet -previousView;
				pm.melGlobals['tk_toggleFrame']=0
				print("frame vertex " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
		if mode == 1 and maskEdge == 1 and len(selection) != 0:
			if not pm.melGlobals['tk_toggleFrame'] == 1:
				pm.viewFit(fitFactor=.3)
				pm.melGlobals['tk_toggleFrame']=1
				print("frame edge " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
			else:
				pm.viewFit(fitFactor=.9)
				#viewSet -previousView;
				pm.melGlobals['tk_toggleFrame']=0
				print("frame edge " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
		if mode == 1 and maskFacet == 1:
			if not pm.melGlobals['tk_toggleFrame'] == 1:
				pm.viewFit(fitFactor=.9)
				pm.melGlobals['tk_toggleFrame']=1
				print("frame facet " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
			else:
				pm.viewFit(fitFactor=.45)
				#viewSet -previousView;
				pm.melGlobals['tk_toggleFrame']=0
				print("frame facet " + str(pm.melGlobals['tk_toggleFrame']) + "\n")

		elif mode == 0 and len(selection) != 0:
			if not pm.melGlobals['tk_toggleFrame'] == 1:
				pm.viewFit(fitFactor=.99)
				pm.melGlobals['tk_toggleFrame']=1
				print("frame object " + str(pm.melGlobals['tk_toggleFrame']) + "\n")
			
			else:
				pm.viewFit(fitFactor=.65)
				#viewSet -previousView;
				pm.melGlobals['tk_toggleFrame']=0
				print("frame object " + str(pm.melGlobals['tk_toggleFrame']) + "\n")


	@staticmethod
	def hk_wireframe_on_shaded():
		'''
		hk_wireframe_on_shaded
		Toggle wireframe on shaded
		'''
		currentPanel = pm.getPanel(withFocus=True)
		mode = pm.displayPref(query=True, wireframeOnShadedActive=True)

		if mode=='none':
			pm.displayPref(wireframeOnShadedActive='reduced')
			Macros.setWireframeOnShadedOption(currentPanel, 1)
			pm.inViewMessage(statusMessage="<hl>Wireframe-on-selection</hl> is now <hl>Full</hl>.\\n<hl>3</hl>", pos='topCenter', fade=True)

		if mode=='reduced':
			pm.displayPref(wireframeOnShadedActive='full')
			Macros.setWireframeOnShadedOption(currentPanel, 0)
			pm.inViewMessage(statusMessage="<hl>Wireframe-on-selection</hl> is now <hl>Reduced</hl>.\\n<hl>3</hl>", pos='topCenter', fade=True)

		if mode=='full':
			pm.displayPref(wireframeOnShadedActive='none')
			Macros.setWireframeOnShadedOption(currentPanel, 0)
			pm.inViewMessage(statusMessage="<hl>Wireframe-on-selection</hl> is now <hl>OFF</hl>.\\n<hl>3</hl>", pos='topCenter', fade=True)



	@staticmethod
	def hk_xray():
		'''
		hk_xray
		Toggle xray mode
		Toggle xRay all
		'''
		#xray all except selected
		scene = pm.ls(visible=1, dag=1, noIntermediate=1, flatten=1, type='surfaceShape')
		selection = pm.ls(shapes=1, selection=1, dagObjects=1)
		for obj in scene:
			if not obj in selection:
				state = pm.displaySurface(obj, xRay=1, query=1)
				pm.displaySurface(obj, xRay=(not state[0]))



	@staticmethod
	def hk_wireframe():
		'''
		hk_wireframe
		Toggle wireframe/shaded/shaded w/texture display
		'''
		currentPanel = pm.getPanel(withFocus=1)
		state = pm.modelEditor(currentPanel, query=1, displayAppearance=1)
		displayTextures = pm.modelEditor(currentPanel, query=1, displayTextures=1)

		if pm.modelEditor(currentPanel, exists=True):
			if not state=="wireframe" and displayTextures==False:
				pm.modelEditor(currentPanel, edit=1, displayAppearance='smoothShaded', activeOnly=False, displayTextures=True)
				pm.inViewMessage(statusMessage="modelEditor smoothShaded <hl>True</hl> displayTextures <hl>True</hl>.\\n<hl>5</hl>", pos='topCenter', fade=True)

			if state=="wireframe" and displayTextures==True:
				pm.modelEditor(currentPanel, edit=1, displayAppearance='smoothShaded', activeOnly=False, displayTextures=False)
				pm.inViewMessage(statusMessage="modelEditor smoothShaded <hl>True</hl> displayTextures <hl>False</hl>.\\n<hl>5</hl>", pos='topCenter', fade=True)

			if not state=="wireframe" and displayTextures==True:
				pm.modelEditor(currentPanel, edit=1, displayAppearance='wireframe', activeOnly=False)
				pm.inViewMessage(statusMessage="modelEditor Wireframe <hl>True</hl>.\\n<hl>5</hl>", pos='topCenter', fade=True)



	@staticmethod
	def hk_shading():
		'''
		hk_shading
		Toggle viewport shading
		'''
		currentPanel = pm.getPanel (withFocus=1)
		displayAppearance = pm.modelEditor (currentPanel, query=1, displayAppearance=1)
		displayTextures = pm.modelEditor (currentPanel, query=1, displayTextures=1)
		displayLights = pm.modelEditor (currentPanel, query=1, displayLights=1)

		#print(displayAppearance, displayTextures, displayLights)
		if pm.modelEditor (currentPanel, exists=1):
			if all ([displayAppearance=="wireframe", displayTextures==False, displayLights=="default"]):
				pm.modelEditor (currentPanel, edit=1, displayAppearance="smoothShaded", displayTextures=False, displayLights="default") #textures off
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>false</hl>.\n<hl>4</hl>", fade=True, position="topCenter")
			elif all ([displayAppearance=="smoothShaded", displayTextures==False, displayLights=="default"]):
				pm.modelEditor (currentPanel, edit=1, displayAppearance="smoothShaded", displayTextures=True, displayLights="default") #textures on
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")	
			elif all ([displayAppearance=="smoothShaded", displayTextures==True, displayLights=="default"]):
				pm.modelEditor (currentPanel, edit=1, displayAppearance="smoothShaded", displayTextures=True, displayLights="active") #lighting on
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayLights <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")	
			else: #use else for starting condition in case settings are changed elsewhere and none of the conditions are met:
				pm.modelEditor (currentPanel, edit=1, displayAppearance="wireframe", displayTextures=False, displayLights="default") #wireframe
				pm.inViewMessage (statusMessage="modelEditor -wireframe <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")



	# Edit -----------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def hk_selection_mode():
		'''
		hk_selection_mode
		Toggle between object selection & last component selection
		'''
		objectMode = pm.selectMode(query=True, object=True)
		if objectMode:
			pm.selectMode(component=True)
		else:
			pm.selectMode(object=True)


	@staticmethod
	def hk_paste_and_rename():
		'''
		hk_paste_and_rename
		Paste and rename removing keyword 'paste'
		'''
		pm.mel.cutCopyPaste("paste")
		#paste and then re-name object removing keyword 'pasted'
		pasted=pm.ls("pasted__*")
		object = ""
		for object in pasted:
			elements = []
			# The values returned by ls may be full or partial dag
			# paths - when renaming we only want the actual
			# object name so strip off the leading dag path.
			#
			elements=object.split("|")
			stripped=elements[- 1]
			# Remove the 'pasted__' suffix from the name
			#
			stripped=stripped.replace("pasted__","")
			# When renaming a transform its shape will automatically be
			# be renamed as well. Use catchQuiet here to ignore errors
			# when trying to rename the child shape a second time.
			# 
			pm.catch(lambda: pm.evalEcho("rename " + str(object) + " " + stripped))



	@staticmethod
	def hk_multi_component():
		'''
		hk_multi_component
		Multi-Component Selection
		'''
		pm.SelectMultiComponentMask()
		pm.inViewMessage(statusMessage="<hl>Multi-Component Selection Mode</hl>\\n Mask is now <hl>ON</hl>.\\n<hl>F4</hl>", fade=True, position="topCenter")



	@staticmethod
	def hk_toggle_component_mask():
		'''
		hk_toggle_component_mask
		Toggle Component Selection Mask
		'''
		mode=pm.selectMode(query=1, component=1)
		if mode == 0:
			pm.mel.changeSelectMode('-component')
			
		maskVertex=pm.selectType(query=1, vertex=1)
		maskEdge=pm.selectType(query=1, edge=1)
		maskFacet=pm.selectType(facet=1, query=1)
		if maskEdge == 0 and maskFacet == 1:
			pm.selectType(vertex=True)
			pm.inViewMessage(position='topCenter', fade=1, statusMessage="<hl>Vertex</hl> Mask is now <hl>ON</hl>.\n<hl>F4</hl>")
			
		if maskVertex == 1 and maskFacet == 0:
			pm.selectType(edge=True)
			pm.inViewMessage(position='topCenter', fade=1, statusMessage="<hl>Edge</hl> Mask is now <hl>ON</hl>.\n<hl>F4</hl>")
			
		if maskVertex == 0 and maskEdge == 1:
			pm.selectType(facet=True)
			pm.inViewMessage(position='topCenter', fade=1, statusMessage="<hl>Facet</hl> Mask is now <hl>ON</hl>.\n<hl>F4</hl>")




	#UI --------------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def hk_tk_show():
		'''
		hk_tk_show
		Display tk marking menu
		'''
		if 'tk' not in locals() and 'tk' not in globals():
			from tk_maya import Instance
			tk = Instance()

		tk.show_()



	@staticmethod
	def hk_hotbox_full():
		'''
		hk_hotbox_full
		Display the full version of the hotbox
		'''
		pm.hotBox(polygonsOnlyMenus=1, displayHotbox=1)
		pm.hotBox()



	@staticmethod
	def hk_toggle_panels():
		'''
		hk_toggle_panels
		Toggle UI toolbars
		'''
		if pm.menu('MayaWindow|HotBoxControlsMenu', q=1, ni=1) == 0:
			pm.setParent('MayaWindow|HotBoxControlsMenu', m=1)
			# added this expression to fix 'toggleMainMenubar function not found' error
			pm.mel.source('HotboxControlsMenu')

		#toggle panel menus
		panels=pm.getPanel(allPanels=1)
		state=int(pm.panel(panels[0], menuBarVisible=1, query=1))
		for panel in panels:
			pm.panel(panel, edit=1, menuBarVisible=(not state))
			# int $state = `panel -query -menuBarVisible $panel`;
			
		pm.mel.toggleMainMenubar(not state)
		#toggle main menubar
		#toggle titlebar
		pm.window(gMainWindow, edit=1, titleBar=(not state))

		# //toggle fullscreen mode //working but issues with windows resizing on toggle
		# inFullScreenMode=int(pm.optionVar(q="workspacesInFullScreenUIMode"))
		# inZoomInMode=int(pm.optionVar(q="workspacesInZoomInUIMode"))
		# # enter full screen mode only if the zoom-in mode is not active.
		# if not inZoomInMode:
		# 	panelWithFocus=str(pm.getPanel(withFocus=1))
		# 	parentControl=str(pm.workspaceLayoutManager(parentWorkspaceControl=panelWithFocus))
		# 	isFloatingPanel=int(pm.workspaceControl(parentControl, q=1, floating=1))
		# 	if not isFloatingPanel:
		# 		if inFullScreenMode:
		# 			pm.workspaceLayoutManager(restoreMainWindowControls=1)
		# 			#come out of fullscreen mode
					
				
		# 		else:
		# 			pm.workspaceLayoutManager(collapseMainWindowControls=(parentControl, True))
		# 			# enter fullscreen mode
					
		# 		pm.optionVar(iv=("workspacesInFullScreenUIMode", (not inFullScreenMode)))
				






# -----------------------------------------------
# Notes
# -----------------------------------------------

'''
#create wrapper
mel.createMelWrapper(method)

#set command
pm.nameCommand('name', annotation='', command=<>)
pm.hotkey(key='1', altModifier=True, name='name')


#clear keyboard shortcut
pm.hotkey(keyShortcut=key, name='', releaseName='', ctl=ctl, alt=alt, sht=sht) #unset the key press name and releaseName.


#query runTimeCommand
if pm.runTimeCommand('name', exists=True):


#delete runTimeCommand
pm.runTimeCommand('name', edit=True, delete=True)


#set runTimeCommand
pm.runTimeCommand(
			'name',
			annotation=string,
			category=string,
			categoryArray,
			command=script,
			commandArray,
			commandLanguage=string,
			default=boolean,
			defaultCommandArray,
			delete,
			exists,
			hotkeyCtx=string,
			image=string,
			keywords=string,
			annotation=string,
			longAnnotation=string,
			numberOfCommands,
			numberOfDefaultCommands,
			numberOfUserCommands,
			plugin=string,
			save,
			showInHotkeyEditor=boolean,
			tags=string,
			userCommandArray,
)

-annotation(-ann) string createqueryedit 
		Description of the command.

-category(-cat) string createqueryedit	
		Category for the command.

-categoryArray(-caa) query			
		Return all the run time command categories.

-command(-c) script createqueryedit		
		Command to be executed when runTimeCommand is invoked.

-commandArray(-ca) query				
		Returns an string array containing the names of all the run time commands.

-commandLanguage(-cl) string createqueryedit
		In edit or create mode, this flag allows the caller to choose a scripting language for a command passed to the "-command" flag. If this flag is not specified, then the callback will be assumed to be in the language from which the runTimeCommand command was called. In query mode, the language for this runTimeCommand is returned. The possible values are "mel" or "python".

-default(-d) boolean createquery 		
		Indicate that this run time command is a default command. Default run time commands will not be saved to preferences.

-defaultCommandArray(-dca) query				
		Returns an string array containing the names of all the default run time commands.

-delete(-del) edit 				
		Delete the specified user run time command.

-exists(-ex) create 				
		Returns true|false depending upon whether the specified object exists. Other flags are ignored.

-hotkeyCtx(-hc)	string createqueryedit 	
		hotkey Context for the command.

-image(-i) string createqueryedit 	
		Image filename for the command.

-keywords(-k) string createqueryedit		
		Keywords for the command. Used for searching for commands in Type To Find. When multiple keywords, use ; as a separator. (Example: "keyword1;keyword2")

-annotation(-annotation) string createqueryedit		
		Label for the command.

-longAnnotation(-la) string createqueryedit	
		Extensive, multi-line description of the command. This will show up in Type To Finds more info page in addition to the annotation.

-numberOfCommands(-nc) query			
		Return the number of run time commands.

-numberOfDefaultCommands(-ndc) query			
		Return the number of default run time commands.

-numberOfUserCommands(-nuc)	query			
		Return the number of user run time commands.

-plugin(-p)	string createqueryedit			
		Name of the plugin this command requires to be loaded. This flag wraps the script provided into a safety check and automatically loads the plugin referenced on execution if it hasn't been loaded. If the plugin fails to load, the command won't be executed.

-save(-s) edit 							
		Save all the user run time commands.

-showInHotkeyEditor(-she) boolean createqueryedit		
		Indicate that this run time command should be shown in the Hotkey Editor. Default value is true.

-tags(-t) string createqueryedit	
		Tags for the command. Used for grouping commands in Type To Find. When more than one tag, use ; as a separator. (Example: "tag1;tag2")

-userCommandArray(-uca)	query			
		Returns an string array containing the names of all the user run time commands.
'''



# Depricated: -------------------------------------------------------------------------------------------------------




		# string $image_plane[] = `ls -exactType imagePlane`;
		# for ($object in $image_plane){
		# 	if (`getAttr ($object+".displayMode")` != 2){
		# 		setAttr ($object+".displayMode") 2;
		# 		grid -toggle 1;
		# 		inViewMessage -statusMessage "Grid is now <hl>ON</hl>.\\n<hl>F1</hl>"  -fade -position topCenter;
		# 	}else{
		# 		setAttr ($object+".displayMode") 0;
		# 		grid -toggle 0;
		# 		inViewMessage -statusMessage "Grid is now <hl>OFF</hl>.\\n<hl>F1</hl>"  -fade -position topCenter;
		# 	}
		# }


# 		global int $tk_toggleFrame;

# 		string $selection[] = `ls -selection`;

# 		$mode = `selectMode -query -component`;
# 		$maskVertex = `selectType -query -vertex`;
# 		$maskEdge = `selectType -query -edge`;
# 		$maskFacet = `selectType -query -facet`;

# 		if (size($selection)==0)
# 			{
# 			viewFit -allObjects;
# 			}
			
# 		if ($mode==1 && $maskVertex==1 && size($selection)!=0)
# 			{
# 			if (size($selection)>1)
# 				{
# 				if ($tk_toggleFrame == !1)
# 					{
# 					viewFit -fitFactor .65;
# 					$tk_toggleFrame = 1;
# 					print ("frame vertices "+$tk_toggleFrame+"\\n");
# 					}
# 				else
# 					{
# 					viewFit -fitFactor .10;
# 					//viewSet -previousView;
# 					$tk_toggleFrame = 0;
# 					print ("frame vertices "+$tk_toggleFrame+"\\n");
# 					}
# 				}
# 			else
# 				{
# 				if ($tk_toggleFrame == !1)
# 					{
# 					viewFit -fitFactor .15;
# 					$tk_toggleFrame = 1;
# 					print ("frame vertex "+$tk_toggleFrame+"\\n");
# 					}
# 				else
# 					{
# 					viewFit -fitFactor .01;
# 					//viewSet -previousView;
# 					$tk_toggleFrame = 0;
# 					print ("frame vertex "+$tk_toggleFrame+"\\n");
# 					}
# 				}
# 			}
# 		if ($mode==1 && $maskEdge==1 && size($selection)!=0)
# 			{
# 			if ($tk_toggleFrame == !1)
# 				{
# 				viewFit -fitFactor .3;
# 				$tk_toggleFrame = 1;
# 				print ("frame edge "+$tk_toggleFrame+"\\n");
# 				}
# 			else
# 				{
# 				viewFit -fitFactor .9;
# 				//viewSet -previousView;
# 				$tk_toggleFrame = 0;
# 				print ("frame edge "+$tk_toggleFrame+"\\n");
# 				}
# 			}
# 		if ($mode==1 && $maskFacet==1)
# 			{
# 			if ($tk_toggleFrame == !1)
# 				{
# 				viewFit -fitFactor .9;
# 				$tk_toggleFrame = 1;
# 				print ("frame facet "+$tk_toggleFrame+"\\n");
# 				}
# 			else
# 				{
# 				viewFit -fitFactor .45;
# 				//viewSet -previousView;
# 				$tk_toggleFrame = 0;
# 				print ("frame facet "+$tk_toggleFrame+"\\n");
# 				}
# 			}
# 		else if ($mode==0  && size($selection)!=0)
# 			{
# 			if ($tk_toggleFrame == !1)
# 				{
# 				viewFit -fitFactor .99;
# 				$tk_toggleFrame = 1;
# 				print ("frame object "+$tk_toggleFrame+"\\n");
# 				}
# 			else
# 				{
# 				viewFit -fitFactor .65;
# 				//viewSet -previousView;
# 				$tk_toggleFrame = 0;
# 				print ("frame object "+$tk_toggleFrame+"\\n");
# 				}
# 			}




		# string $currentPanel = `getPanel -withFocus`;
		# $mode = `displayPref -query -wireframeOnShadedActive`;

		# if ($mode=="none")
		# 	{
		# 	displayPref -wireframeOnShadedActive "reduced";
		# 	setWireframeOnShadedOption 1 $currentPanel;
		# 	inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>Full</hl>.\\n<hl>3</hl>"  -fade -position topCenter;
		# 	}
		# if ($mode=="reduced")
		# 	{
		# 	displayPref -wireframeOnShadedActive "full";
		# 	setWireframeOnShadedOption 0 $currentPanel;
		# 	inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>Reduced</hl>.\\n<hl>3</hl>"  -fade -position topCenter;
		# 	}
		# if ($mode=="full")
		# 	{
		# 	displayPref -wireframeOnShadedActive "none";
		# 	setWireframeOnShadedOption 0 $currentPanel;
		# 	inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>OFF</hl>.\\n<hl>3</hl>" -fade -position topCenter;
		# 	}


	# //xray all except selected
	# string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
	# string $selection[] = `ls -selection -dagObjects -shapes`;
	# for ($object in $scene)
	# 	{
	# 	if (!stringArrayContains ($object, $selection))
	# 		{
	# 		int $state[] = `displaySurface -query -xRay $object`;
	# 		displaySurface -xRay ( !$state[0] ) $object;
	# 		}
	# 	}


		# mel.eval('''
		# string $currentPanel = `getPanel -withFocus`;
		# string $state = `modelEditor -query -displayAppearance $currentPanel`;
		# string $displayTextures = `modelEditor -query -displayTextures $currentPanel`;
		# if(`modelEditor -exists $currentPanel`)
		#   {
		# 	if($state != "wireframe" && $displayTextures == false)
		# 	  {
		# 		modelEditor -edit -displayAppearance smoothShaded -activeOnly false -displayTextures true $currentPanel;
		# 		inViewMessage -statusMessage "modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>true</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
		# 		}
		# 	if($state == "wireframe" && $displayTextures == true)
		# 	  {
		# 		modelEditor -edit -displayAppearance smoothShaded -activeOnly false -displayTextures false $currentPanel;
		# 		inViewMessage -statusMessage "modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>false</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
		# 		}
		# 	if($state != "wireframe" && $displayTextures == true)
		# 	  {
		# 		modelEditor -edit -displayAppearance wireframe -activeOnly false $currentPanel;
		# 		inViewMessage -statusMessage "modelEditor -wireframe <hl>true</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
		# 		}
		# 	}
		# ''')


# SelectMultiComponentMask;
# inViewMessage -statusMessage "<hl>Multi-Component Selection Mode</hl>\\n Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;



		# //paste and then re-name object removing keyword 'pasted'
		# cutCopyPaste "paste";
		# {
		# string $pasted[] = `ls "pasted__*"`;
		# string $object;
		# for ( $object in $pasted )
		# {
		# string $elements[];
		# // The values returned by ls may be full or partial dag
		# // paths - when renaming we only want the actual
		# // object name so strip off the leading dag path.
		# //
		# tokenize( $object, "|", $elements );
		# string $stripped = $elements[ `size $elements` - 1 ];
		# // Remove the 'pasted__' suffix from the name
		# //
		# $stripped = `substitute "pasted__" $stripped ""`;
		# // When renaming a transform its shape will automatically be
		# // be renamed as well. Use catchQuiet here to ignore errors
		# // when trying to rename the child shape a second time.
		# // 
		# catchQuiet(`evalEcho("rename " + $object + " " + $stripped)`);
		# }
		# };
		# //alternative: edit the cutCopyPaste.mel
		# //REMOVE the line "-renameAll" so the sub-nodes won't get renamed at all
		# //REMOVE the -renamingPrefix "paste_" line
		# //and instead write the line -defaultNamespace


# $mode = `selectMode -query -component`;
# if ($mode==0)
#   {
# 	changeSelectMode -component;
# 	}

# $maskVertex = `selectType -query -vertex`;
# $maskEdge = `selectType -query -edge`;
# $maskFacet = `selectType -query -facet`;

# if ($maskEdge==0 && $maskFacet==1)
# 	{
# 	selectType -vertex true;
# 	inViewMessage -statusMessage "<hl>Vertex</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
# 	}
# if ($maskVertex==1 && $maskFacet==0)
# 	{
# 	selectType -edge true;
# 	inViewMessage -statusMessage "<hl>Edge</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
# 	}
# if ($maskVertex==0 && $maskEdge==1)
# 	{
# 	selectType -facet true;
# 	inViewMessage -statusMessage "<hl>Facet</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
# 	}


		# // added this expression to fix 'toggleMainMenubar function not found' error
		# if (`menu -q -ni MayaWindow|HotBoxControlsMenu` == 0) {setParent -m MayaWindow|HotBoxControlsMenu;source HotboxControlsMenu;};

		# //toggle panel menus
		# string $panels[] = `getPanel -allPanels`;
		# int $state = `panel -query -menuBarVisible $panels[0]`;
		# for ($panel in $panels)
		# {
		# 	// int $state = `panel -query -menuBarVisible $panel`;
		# 	panel -edit -menuBarVisible (!$state) $panel;
		# }
		# //toggle main menubar
		# toggleMainMenubar (!$state);

		# //toggle titlebar
		# window -edit -titleBar (!$state) $gMainWindow;

		# // //toggle fullscreen mode //working but issues with windows resizing on toggle
		# // int $inFullScreenMode = `optionVar -q "workspacesInFullScreenUIMode"`;
		# // int $inZoomInMode = `optionVar -q "workspacesInZoomInUIMode"`;
		# // // enter full screen mode only if the zoom-in mode is not active.
		# // if(!$inZoomInMode) 
		# // {
		# // 	string $panelWithFocus = `getPanel -withFocus`;
		# // 	string $parentControl = `workspaceLayoutManager -parentWorkspaceControl $panelWithFocus`;
		# // 	int $isFloatingPanel = `workspaceControl -q -floating $parentControl`;
						
		# // 	if(!$isFloatingPanel) 
		# // 	{
		# // 		if($inFullScreenMode) 
		# // 		{
		# // 		//come out of fullscreen mode
		# // 		workspaceLayoutManager -restoreMainWindowControls;
		# // 		}
		# // 		else 
		# // 		{
		# // 			// enter fullscreen mode
		# // 			workspaceLayoutManager -collapseMainWindowControls $parentControl true;
		# // 		}
		# // 	optionVar -iv "workspacesInFullScreenUIMode" (!$inFullScreenMode);
		# // 	}
		# // }