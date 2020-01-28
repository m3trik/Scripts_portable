import pymel.core as pm
import maya.mel as mel


import tk_maya
tk = tk_maya.Tk_maya()



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
		self.setMacro(name='hk_back_face_culling', k='1', cat='Display', ann='Toggle back-face culling')
		self.setMacro(name='hk_smooth_preview', k='2', cat='Display', ann='Toggle smooth mesh preview')
		self.setMacro(name='hk_isolate_selected', k='F2', cat='Display', ann='Isolate current selection')
		self.setMacro(name='hk_grid_and_image_planes', k='F1', cat='Display', ann='Toggle grid and image plane visibility')
		self.setMacro(name='hk_frame_selected', k='f', cat='Display', ann='Frame selected by a set amount')
		self.setMacro(name='hk_wireframe_on_shaded', k='3', cat='Display', ann='Toggle wireframe on shaded')
		self.setMacro(name='hk_xray', k='F3', cat='Display', ann='Toggle xRay all')
		self.setMacro(name='hk_wireframe', k='5', cat='Display', ann='Toggle wireframe/shaded/shaded w/texture display')
		self.setMacro(name='hk_shading', k='6', cat='Display', ann='Toggle viewport shading')
		self.setMacro(name='hk_selection_mode', k='sht+q', cat='Edit', ann='Toggle between object selection & last component selection')
		self.setMacro(name='hk_paste_and_rename', k='ctl+v', cat='Edit', ann='Paste and rename removing keyword "paste"')
		self.setMacro(name='hk_multi_component', k='F5', cat='Edit', ann='Multi-Component Selection')
		self.setMacro(name='hk_toggle_component_mask', k='F4', cat='Edit', ann='Toggle Component Selection Mask')
		self.setMacro(name='hk_tk_show', k='F12', cat='UI', ann='Display tk marking menu')
		self.setMacro(name='hk_hotbox_full', k='sht+z', cat='UI', ann='Display the full version of the hotbox')
		self.setMacro(name='hk_toggle_panels', k='9', cat='UI', ann='Toggle UI toolbars')


	def setMacro(self, name=None, k=None, cat=None, ann=None):
		'''
		Sets a default runtime command with a keyboard shotcut.
		args:
			name = 'string' - The command name you provide must be unique. The name itself must begin with an alphabetic character or underscore followed by alphanumeric characters or underscores.
			cat = 'string' - catagory - Category for the command.
			ann = 'string' - annotation - Description of the command.
			k = 'string' - keyShortcut - Specify what key is being set.
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
		command = "from macros import Macros; Macros.{0}();".format(name)

		#set command
		nameCommand = pm.nameCommand(
				'{0}Command'.format(name),
				annotation=ann,
				command='python("{0}")'.format(command),
		)

		#set runTimeCommand
		pm.runTimeCommand(
				name,
				annotation=ann,
				category=cat,
				command=command,
				default=True,
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

		# print name, char, ctl, alt, sht
		pm.hotkey(keyShortcut=key, name=name, ctl=ctl, alt=alt, sht=sht) #set only the key press.



	# Display --------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def hk_back_face_culling():
		'''
		hk_back_face_culling
		Toggle Back-Face Culling
		1
		'''
		mel.eval('''
		string $selection[] = `ls -selection`;//-transforms (all transform objects)
		int $query[] = `polyOptions -query -wireBackCulling`;
		if ($query[0] != 1){
				polyOptions -global -wireBackCulling;
				setWireframeOnShadedOption 1 (`getPanel -withFocus`);
				inViewMessage -statusMessage "Back-Face Culling is now <hl>OFF</hl>.\\n<hl>1</hl>"  -fade -position topCenter;
			}else{
				polyOptions -global -backCulling;
				setWireframeOnShadedOption 0 (`getPanel -withFocus`);
				inViewMessage -statusMessage "Back-Face Culling is now <hl>ON</hl>.\\n<hl>1</hl>"  -fade -position topCenter;
			}
		''')


	@staticmethod
	def hk_smooth_preview():
		'''
		hk_smooth_preview
		Toggle smooth mesh preview
		2
		'''
		mel.eval('''
		string $selection[] = `ls -selection`;
		string $scene[] = `ls -geometry`;

		//if no object selected smooth all geometry
		if (size($selection)==0)
			{
			for ($object in $scene)
			{
			if (`getAttr ($object+".displaySmoothMesh")` != 2)
				{
				setAttr  ($object+".displaySmoothMesh") 2;//smooth preview on
				displayPref -wireframeOnShadedActive "none";//selection wireframe off
				inViewMessage -statusMessage "S-Div Preview is now <hl>ON</hl>.\\n<hl>2</hl>"  -fade -position topCenter;
				}
			else
				{
				setAttr  ($object+".displaySmoothMesh") 0;//smooth preview off
				displayPref -wireframeOnShadedActive "full";//selection wireframe on
				inViewMessage -statusMessage "S-Div Preview is now <hl>OFF</hl>.\\n<hl>2</hl>"  -fade -position topCenter;
				}
			if (`getAttr ($object+".smoothLevel")` != 1)
				{
				setAttr  ($object+".smoothLevel") 1;
				}
			}
			}

		//smooth selection only
		for ($object in $selection)
			{
			if (`getAttr ($object+".displaySmoothMesh")` != 2)
				{
				setAttr  ($object+".displaySmoothMesh") 2;//smooth preview on
				displayPref -wireframeOnShadedActive "none";//selection wireframe off
				inViewMessage -statusMessage "S-Div Preview is now <hl>ON</hl>.\\n<hl>2</hl>"  -fade -position topCenter;
				}
			else
				{
				setAttr  ($object+".displaySmoothMesh") 0;//smooth preview off
				displayPref -wireframeOnShadedActive "full";//selection wireframe on
				inViewMessage -statusMessage "S-Div Preview is now <hl>OFF</hl>.\\n<hl>2</hl>"  -fade -position topCenter;
				}
			if (`getAttr ($object+".smoothLevel")` != 1)
				{
				setAttr  ($object+".smoothLevel") 1;
				}
			}
		''')


	@staticmethod
	def hk_isolate_selected():
		'''
		hk_isolate_selected
		Isolate current selection
		F2
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
		F1
		'''
		mel.eval('''
		string $image_plane[] = `ls -exactType imagePlane`;
		for ($object in $image_plane){
			if (`getAttr ($object+".displayMode")` != 2){
				setAttr ($object+".displayMode") 2;
				grid -toggle 1;
				inViewMessage -statusMessage "Grid is now <hl>ON</hl>.\\n<hl>F1</hl>"  -fade -position topCenter;
			}else{
				setAttr ($object+".displayMode") 0;
				grid -toggle 0;
				inViewMessage -statusMessage "Grid is now <hl>OFF</hl>.\\n<hl>F1</hl>"  -fade -position topCenter;
			}
		}
		''')


	@staticmethod
	def hk_frame_selected():
		'''
		hk_frame_selected
		Frame selected by a set amount
		F
		'''
		mel.eval('''
		global int $tk_toggleFrame;

		string $selection[] = `ls -selection`;

		$mode = `selectMode -query -component`;
		$maskVertex = `selectType -query -vertex`;
		$maskEdge = `selectType -query -edge`;
		$maskFacet = `selectType -query -facet`;

		if (size($selection)==0)
			{
			viewFit -allObjects;
			}
			
		if ($mode==1 && $maskVertex==1 && size($selection)!=0)
			{
			if (size($selection)>1)
				{
				if ($tk_toggleFrame == !1)
					{
					viewFit -fitFactor .65;
					$tk_toggleFrame = 1;
					print ("frame vertices "+$tk_toggleFrame+"\\n");
					}
				else
					{
					viewFit -fitFactor .10;
					//viewSet -previousView;
					$tk_toggleFrame = 0;
					print ("frame vertices "+$tk_toggleFrame+"\\n");
					}
				}
			else
				{
				if ($tk_toggleFrame == !1)
					{
					viewFit -fitFactor .15;
					$tk_toggleFrame = 1;
					print ("frame vertex "+$tk_toggleFrame+"\\n");
					}
				else
					{
					viewFit -fitFactor .01;
					//viewSet -previousView;
					$tk_toggleFrame = 0;
					print ("frame vertex "+$tk_toggleFrame+"\\n");
					}
				}
			}
		if ($mode==1 && $maskEdge==1 && size($selection)!=0)
			{
			if ($tk_toggleFrame == !1)
				{
				viewFit -fitFactor .3;
				$tk_toggleFrame = 1;
				print ("frame edge "+$tk_toggleFrame+"\\n");
				}
			else
				{
				viewFit -fitFactor .9;
				//viewSet -previousView;
				$tk_toggleFrame = 0;
				print ("frame edge "+$tk_toggleFrame+"\\n");
				}
			}
		if ($mode==1 && $maskFacet==1)
			{
			if ($tk_toggleFrame == !1)
				{
				viewFit -fitFactor .9;
				$tk_toggleFrame = 1;
				print ("frame facet "+$tk_toggleFrame+"\\n");
				}
			else
				{
				viewFit -fitFactor .45;
				//viewSet -previousView;
				$tk_toggleFrame = 0;
				print ("frame facet "+$tk_toggleFrame+"\\n");
				}
			}
		else if ($mode==0  && size($selection)!=0)
			{
			if ($tk_toggleFrame == !1)
				{
				viewFit -fitFactor .99;
				$tk_toggleFrame = 1;
				print ("frame object "+$tk_toggleFrame+"\\n");
				}
			else
				{
				viewFit -fitFactor .65;
				//viewSet -previousView;
				$tk_toggleFrame = 0;
				print ("frame object "+$tk_toggleFrame+"\\n");
				}
			}
		''')


	@staticmethod
	def hk_wireframe_on_shaded():
		'''
		hk_wireframe_on_shaded
		Toggle wireframe on shaded
		3
		'''
		mel.eval('''
		string $current_panel = `getPanel -withFocus`;
		$mode = `displayPref -query -wireframeOnShadedActive`;

		if ($mode=="none")
			{
			displayPref -wireframeOnShadedActive "reduced";
			setWireframeOnShadedOption 1 $current_panel;
			inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>Full</hl>.\\n<hl>3</hl>"  -fade -position topCenter;
			}
		if ($mode=="reduced")
			{
				displayPref -wireframeOnShadedActive "full";
			setWireframeOnShadedOption 0 $current_panel;
			inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>Reduced</hl>.\\n<hl>3</hl>"  -fade -position topCenter;
			}
		if ($mode=="full")
			{
			displayPref -wireframeOnShadedActive "none";
			setWireframeOnShadedOption 0 $current_panel;
			inViewMessage -statusMessage "<hl>Wireframe-on-selection</hl> is now <hl>OFF</hl>.\\n<hl>3</hl>" -fade -position topCenter;
			}
		''')


	@staticmethod
	def hk_xray():
		'''
		hk_xray
		Toggle xray mode
		F3
		Toggle xRay all
		'''
		mel.eval('''
		//xray all except selected
		string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
		string $selection[] = `ls -selection -dagObjects -shapes`;
		for ($object in $scene)
			{
			if (!stringArrayContains ($object, $selection))
				{
				int $state[] = `displaySurface -query -xRay $object`;
				displaySurface -xRay ( !$state[0] ) $object;
				}
			}
		''')


	@staticmethod
	def hk_wireframe():
		'''
		hk_wireframe
		Toggle wireframe/shaded/shaded w/texture display
		5
		'''
		mel.eval('''
		string $current_panel = `getPanel -withFocus`;
		string $state = `modelEditor -query -displayAppearance $current_panel`;
		string $displayTextures = `modelEditor -query -displayTextures $current_panel`;
		if(`modelEditor -exists $current_panel`)
		  {
			if($state != "wireframe" && $displayTextures == false)
			  {
				modelEditor -edit -displayAppearance smoothShaded -activeOnly false -displayTextures true $current_panel;
				inViewMessage -statusMessage "modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>true</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
				}
			if($state == "wireframe" && $displayTextures == true)
			  {
				modelEditor -edit -displayAppearance smoothShaded -activeOnly false -displayTextures false $current_panel;
				inViewMessage -statusMessage "modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>false</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
				}
			if($state != "wireframe" && $displayTextures == true)
			  {
				modelEditor -edit -displayAppearance wireframe -activeOnly false $current_panel;
				inViewMessage -statusMessage "modelEditor -wireframe <hl>true</hl>.\\n<hl>5</hl>"  -fade -position topCenter;
				}
			}
		''')


	@staticmethod
	def hk_shading():
		'''
		hk_shading
		Toggle viewport shading
		6
		'''
		current_panel = pm.getPanel (withFocus=1)
		displayAppearance = pm.modelEditor (current_panel, query=1, displayAppearance=1)
		displayTextures = pm.modelEditor (current_panel, query=1, displayTextures=1)
		displayLights = pm.modelEditor (current_panel, query=1, displayLights=1)

		#print displayAppearance, displayTextures, displayLights
		if pm.modelEditor (current_panel, exists=1):
			if all ([displayAppearance=="wireframe", displayTextures==False, displayLights=="default"]):
				pm.modelEditor (current_panel, edit=1, displayAppearance="smoothShaded", displayTextures=False, displayLights="default") #textures off
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>false</hl>.\n<hl>4</hl>", fade=True, position="topCenter")
			elif all ([displayAppearance=="smoothShaded", displayTextures==False, displayLights=="default"]):
				pm.modelEditor (current_panel, edit=1, displayAppearance="smoothShaded", displayTextures=True, displayLights="default") #textures on
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayTextures <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")	
			elif all ([displayAppearance=="smoothShaded", displayTextures==True, displayLights=="default"]):
				pm.modelEditor (current_panel, edit=1, displayAppearance="smoothShaded", displayTextures=True, displayLights="active") #lighting on
				pm.inViewMessage (statusMessage="modelEditor -smoothShaded <hl>true</hl> -displayLights <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")	
			else: #use else for starting condition in case settings are changed elsewhere and none of the conditions are met:
				pm.modelEditor (current_panel, edit=1, displayAppearance="wireframe", displayTextures=False, displayLights="default") #wireframe
				pm.inViewMessage (statusMessage="modelEditor -wireframe <hl>true</hl>.\n<hl>4</hl>", fade=True, position="topCenter")



	# Edit -----------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def hk_selection_mode():
		'''
		hk_selection_mode
		Toggle between object selection & last component selection
		sht+q
		'''
		mel.eval('toggleSelMode;')


	@staticmethod
	def hk_paste_and_rename():
		'''
		hk_paste_and_rename
		Paste and rename removing keyword 'paste'
		ctrl+v
		'''
		mel.eval('''
		//paste and then re-name object removing keyword 'pasted'
		cutCopyPaste "paste";
		{
		string $pasted[] = `ls "pasted__*"`;
		string $object;
		for ( $object in $pasted )
		{
		string $elements[];
		// The values returned by ls may be full or partial dag
		// paths - when renaming we only want the actual
		// object name so strip off the leading dag path.
		//
		tokenize( $object, "|", $elements );
		string $stripped = $elements[ `size $elements` - 1 ];
		// Remove the 'pasted__' suffix from the name
		//
		$stripped = `substitute "pasted__" $stripped ""`;
		// When renaming a transform its shape will automatically be
		// be renamed as well. Use catchQuiet here to ignore errors
		// when trying to rename the child shape a second time.
		// 
		catchQuiet(`evalEcho("rename " + $object + " " + $stripped)`);
		}
		};
		//alternative: edit the cutCopyPaste.mel
		//REMOVE the line "-renameAll" so the sub-nodes won't get renamed at all
		//REMOVE the -renamingPrefix "paste_" line
		//and instead write the line -defaultNamespace
		''')


	@staticmethod
	def hk_multi_component():
		'''
		hk_multi_component
		Multi-Component Selection
		f5
		'''
		mel.eval('''
		SelectMultiComponentMask;
		inViewMessage -statusMessage "<hl>Multi-Component Selection Mode</hl>\\n Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
		''')


	@staticmethod
	def hk_toggle_component_mask():
		'''
		hk_toggle_component_mask
		Toggle Component Selection Mask
		f4
		'''
		mel.eval('''
		$mode = `selectMode -query -component`;
		if ($mode==0)
		  {
			changeSelectMode -component;
			}

		$maskVertex = `selectType -query -vertex`;
		$maskEdge = `selectType -query -edge`;
		$maskFacet = `selectType -query -facet`;

		if ($maskEdge==0 && $maskFacet==1)
			{
			selectType -vertex true;
			inViewMessage -statusMessage "<hl>Vertex</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
			}
		if ($maskVertex==1 && $maskFacet==0)
			{
			selectType -edge true;
			inViewMessage -statusMessage "<hl>Edge</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
			}
		if ($maskVertex==0 && $maskEdge==1)
			{
			selectType -facet true;
			inViewMessage -statusMessage "<hl>Facet</hl> Mask is now <hl>ON</hl>.\\n<hl>F4</hl>"  -fade -position topCenter;
			}
		''')



	#UI --------------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def hk_tk_show():
		'''
		hk_tk_show
		Display tk marking menu
		f12
		'''
		global tk

		# if 'tk' not in locals() or 'tk' not in globals():
		# 	import tk_maya
		# 	tk = tk_maya.Tk_maya()

		# elif tk.isVisible():
		# 	tk = tk_maya.Tk_maya()

		# tk.sb.gcProtect(tk)
		tk.show()

		#isActiveWindow ()


	@staticmethod
	def hk_hotbox_full():
		'''
		hk_hotbox_full
		Display the full version of the hotbox
		shft + z
		'''
		mel.eval('''
		hotBox -displayHotbox -polygonsOnlyMenus;
		hotBox;
		''')


	@staticmethod
	def hk_toggle_panels():
		'''
		hk_toggle_panels
		Toggle UI toolbars
		9
		'''
		mel.eval('''
		// added this expression to fix 'toggleMainMenubar function not found' error
		if (`menu -q -ni MayaWindow|HotBoxControlsMenu` == 0) {setParent -m MayaWindow|HotBoxControlsMenu;source HotboxControlsMenu;};

		//toggle panel menus
		string $panels[] = `getPanel -allPanels`;
		int $state = `panel -query -menuBarVisible $panels[0]`;
		for ($panel in $panels)
		{
			// int $state = `panel -query -menuBarVisible $panel`;
			panel -edit -menuBarVisible (!$state) $panel;
		}
		//toggle main menubar
		toggleMainMenubar (!$state);

		//toggle titlebar
		window -edit -titleBar (!$state) $gMainWindow;

		// //toggle fullscreen mode //working but issues with windows resizing on toggle
		// int $inFullScreenMode = `optionVar -q "workspacesInFullScreenUIMode"`;
		// int $inZoomInMode = `optionVar -q "workspacesInZoomInUIMode"`;
		// // enter full screen mode only if the zoom-in mode is not active.
		// if(!$inZoomInMode) 
		// {
		// 	string $panelWithFocus = `getPanel -withFocus`;
		// 	string $parentControl = `workspaceLayoutManager -parentWorkspaceControl $panelWithFocus`;
		// 	int $isFloatingPanel = `workspaceControl -q -floating $parentControl`;
						
		// 	if(!$isFloatingPanel) 
		// 	{
		// 		if($inFullScreenMode) 
		// 		{
		// 		//come out of fullscreen mode
		// 		workspaceLayoutManager -restoreMainWindowControls;
		// 		}
		// 		else 
		// 		{
		// 			// enter fullscreen mode
		// 			workspaceLayoutManager -collapseMainWindowControls $parentControl true;
		// 		}
		// 	optionVar -iv "workspacesInFullScreenUIMode" (!$inFullScreenMode);
		// 	}
		// }
		''')






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


# hk_toggle_outliner
	# OutlinerWindow;



		# command = "from macros import Macros; Macros.{0}();".format(name)

		# #set runTimeCommand
		# pm.runTimeCommand(
		# 		name,
		# 		annotation=ann,
		# 		category=cat,
		# 		command=command,
		# 		default=True,
		# )

		# #set hotkey
		# #modifiers
		# ctl=False; alt=False; sht=False
		# for char in k.split('+'):
		# 	if char=='ctl':
		# 		ctl = True
		# 	elif char=='alt':
		# 		alt = True
		# 	elif char=='sht':
		# 		sht = True
		# 	else:
		# 		key = char

		# print name, char, ctl, alt, sht
		# pm.hotkey(keyShortcut=key, name=name, ctl=ctl, alt=alt, sht=sht) #set only the key press.


		# command = 'python("from macros import Macros; Macros.{0}();")'.format(name)

		# #set command
		# nameCommand = pm.nameCommand(
		# 		'{0}Command'.format(name),
		# 		annotation=ann,
		# 		command=command,
		# )

		# #set runTimeCommand
		# pm.runTimeCommand(
		# 		name,
		# 		annotation=ann,
		# 		category=cat,
		# 		command=nameCommand,
		# 		commandLanguage='mel',
		# 		default=True,
		# )

		# #set hotkey
		# #modifiers
		# ctl=False; alt=False; sht=False
		# for char in k.split('+'):
		# 	if char=='ctl':
		# 		ctl = True
		# 	elif char=='alt':
		# 		alt = True
		# 	elif char=='sht':
		# 		sht = True
		# 	else:
		# 		key = char

		# pm.hotkey(keyShortcut=key, name=name, ctl=ctl, alt=alt, sht=sht) #set only the key press.
