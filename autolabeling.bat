@echo off
if not "%~0"=="%~dp0.\%~nx0" (
     start /min cmd /c,"%~dp0.\%~nx0" %*
     exit
)
set activatePath=\Anaconda3\Scripts\activate.bat
@REM set installedPath=%USERPROFILE%
set installedPath=C:\tools
cd /d %~dp0
call %installedPath%%activatePath%
call activate autolabeling
python main.py