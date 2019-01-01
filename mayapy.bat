@if (@X)==(@Y) @end /* JScript comment
@echo off


rem C:\Program Files\Autodesk\<version>\bin\mayapy.exe needs to be added to PATH environment variable.
rem The initialize routine takes only one parameter (name), and it is optional. The name parameter tells Maya what the name of the application is. The default value for name is python.


rem name of temp file that will perform the imports and the module to import.
set "tmp=standalone.py"
set "module=tk_main"

rem create a temp python file to import maya standalone and run specified the python module.
(
echo import maya.standalone
echo.
echo maya.standalone.initialize(name='python'^)
echo.
echo import %module%
echo maya.standalone.uninitialize(^)
)> %tmp%

rem run the temp file
mayapy %tmp%

pause



rem delete the temp file
del /f %tmp%




