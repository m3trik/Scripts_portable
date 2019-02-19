@if (@X)==(@Y) @end /* JScript comment
@echo off


:: C:\Program Files\Autodesk\3ds Max 2018\3dsmaxpy.exe needs to be added to PATH environment variable.
:: MAXPYTHONPATH is a user defined environment variable that includes 3ds max folders (python and script sub-folders)

:: name of temp file that will perform the imports and the module to import.
set "tmp=__3dsmaxpy__.py"
set "module="

:: create a temp python file to import maya standalone and run specified the python module.
(
echo.
echo "C:/Program Files/Autodesk/3ds Max 2018/3dsmax.exe" -U MAXScript userSetup.ms
)> %tmp%

:: run the temp file
3dsmaxpy.exe %tmp%

pause



:: delete the temp file
del /f %tmp%




