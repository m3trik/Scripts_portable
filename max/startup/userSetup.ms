--------------------------------------------------------------------------------
-- 3ds Max startup script-------------------------------------------------------

--------------------------------------------------------------------------------
-- 3ds Max looks for the Python script under the following directories:

-- User Scripts directory
-- User Startup Scripts directory
-- Scripts directory
-- Startup Scripts
-- Windows paths specified by the Path environment variable. 

-- To see a list of these directories, in your command prompt; enter echo %path%
-- For example, 3ds Max would search under the following directories: 

-- userscripts\python 
-- userscripts\startup\python
-- scripts\python
-- scripts\startup\python
-- subsequently the windows paths.
--------------------------------------------------------------------------------

-- initalize python
python.Init()

--load the python path setup file and user macros.

-- envVar = systemTools.getEnvVariable("CLOUD")
-- fullPath = envVar+"\\____Graphics\\__general\\_portable\\_scripts\\__path\\max\\"
envVar = systemTools.getEnvVariable("USERPROFILE")
fullPath = envVar+"\\Documents\\_portable\\_scripts\\__path\\max\\"

python.ExecuteFile (fullPath+"userSetup.py")
FileIn (fullPath+"tk_macroScript.ms")


-- ui

-- hide statusPanel
statusPanel.visible = true

-- check to see if its open and if not, open the scene explorer
if sceneexplorermanager.ExplorerExists "Scene Explorer" then 
(
	if (not sceneexplorermanager.ExplorerIsOpen "Scene Explorer") then
		sceneexplorermanager.OpenExplorer "Scene Explorer"
)
else
(
	sceneexplorermanager.CreateExplorerFromDefault "Scene Explorer"
)


-- hotkeys
kbdx = actionMan.getKeyboardFile()	--get current keyboard file
actionMan.loadKeyboardFile (kbdx)		--loadKeyboardFile()
-- actionMan.saveKeyboardFile		--saveKeyboardFile()




