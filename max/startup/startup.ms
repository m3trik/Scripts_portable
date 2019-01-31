-- 3ds Max startup script-------------------------------------------------------

-- Maxscipt startup order:
-- MacroScript (MCR) files in ui\macroscripts --not compiled at this time; rather they are just scanned to identify the MacroScripts that have been defined.

-- MAXScript (MS, MSE, and MZP) in the plug-in path directories/subdirectories, and compiles these files. (specified in the Configure System Paths dialog and Configure User Paths dialog) 
-- The base scene and user interface have not been created at this point, so no viewport or scene commands should be executed in these files. 

-- You can prevent a nested directory from being scanned by placing its name in parentheses, for example "(old-versions)"

-- 3ds Max creates the base scene and user interface. Any macro scripts used by buttons in the user interface are compiled at this time.

-- The automatic loading of the following startup script files can be deactivated by turning off the Auto Start MAXScript option in the MAXScript page of the Preferences dialog



--------------------------------------------------------------------------------
-- MAXScript searches for startup.ms in this order: (stop searching when found)

-- The Scripts directory (defined on the Configure User Paths dialog  File I/O panel)
-- The Startup Scripts directory (defined on the Configure System Paths dialog)
-- The 3ds Max executable main directory
-- The Windows system directory (system32)
-- The Windows directory
-- The directories that are listed in the PATH environment variable

-- MAXScript then recursively scans the Startup Scripts directory (defined on the Configure System Paths dialog) and any nested directories for .ms, .mse, and .mzp script files and loads them. 

-- If you specify a script to run in the command line (-U MAXScript script_name)

--------------------------------------------------------------------------------
-- 3ds Max looks for the Python script under the following directories:

-- User Scripts directory
-- User Startup Scripts directory
-- Scripts directory
-- Startup Scripts
-- Windows paths specified by the Path environment variable. 

--------------------------------------------------------------------------------

-- initalize python
python.Init()



--load the python path setup file and user macros.

--get current dir path:
file = getThisScriptFilename() --ie. "C:\__portable\_scripts\max\startup\startup.ms"
dir_ = substring file 1 (findString file ("max")-2) --take substring from index 1 to the index of max in file string


--append to system path:
paths = #(
		dir_,
		dir_+"/tk_ui",
		dir_+"/max",
		dir_+"/max/tk_slots_max"
		)


python.Execute "import sys"
for path_ in paths do
(
	--print ("sys.path.append('"+path_+"')")
	python.Execute ("sys.path.append('"+path_+"')")
)


FileIn (dir_+"/max/macros/macros.ms")




-- hide statusPanel
statusPanel.visible = true

-- check to see if its open and if not, open the scene explorer
-- if sceneexplorermanager.ExplorerExists "Scene Explorer" then 
-- (
-- 	if (not sceneexplorermanager.ExplorerIsOpen "Scene Explorer") then
-- 		sceneexplorermanager.OpenExplorer "Scene Explorer"
-- )
-- else
-- (
-- 	sceneexplorermanager.CreateExplorerFromDefault "Scene Explorer"
-- )





-- hotkeys
kbdx = actionMan.getKeyboardFile()	--get current keyboard file
actionMan.loadKeyboardFile (kbdx)		--loadKeyboardFile()
-- actionMan.saveKeyboardFile		--saveKeyboardFile()









--depricated

--absolute path:
-- USERPROFILE = systemTools.getEnvVariable("USERPROFILE")
-- path_ = USERPROFILE+"\\Documents\\_portable\\_scripts\\__path\\max\\"
-- if not (doesFileExist path_) do
-- (
-- 	CLOUD = systemTools.getEnvVariable("CLOUD")
-- 	path_ = CLOUD+"\\____Graphics\\__general\\_portable\\_scripts\\__path\\max\\"
-- )


-- # ------------------------------------------------
-- # Get the main Max window as a QtGui.QMainWindow instance.
-- # ------------------------------------------------
-- # mainWindow = MaxPlus.GetQMaxMainWindow()


-- # ------------------------------------------------
-- # MaxPlus.FileManager.Reset(True)



-- #Append directory to system path -----------------

-- #add absolute paths:
-- # paths = [
-- # r'%CLOUD%/____Graphics/__general/_portable/_scripts/__path',
-- # r'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/tk_ui',
-- # r'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/max',
-- # r'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/max/tk_slots_max',

-- # r'%USERPROFILE%/Documents/_portable/_scripts/__path',
-- # r'%USERPROFILE%/Documents/_portable/_scripts/__path/tk_ui',
-- # r'%USERPROFILE%/Documents/_portable/_scripts/__path/max',
-- # r'%USERPROFILE%/Documents/_portable/_scripts/__path/max/tk_slots_max'
-- # ]

-- # for path in paths:
-- # 	sys.path.append(os.path.expandvars(path)); #print '%PYTHONPATH%:', path


-- # for s in  sys.path: print s




-- #load tk_main ------------------------------------

-- # if 'tk_main' not in sys.modules:
-- # 	import tk_main #tk_maya_main.py -qt hotbox menus and controls
-- # else:
-- # 	print "reload: tk_main"
-- # 	reload(tk_main)



-- #------------------------------------------------------------------------------