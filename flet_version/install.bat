@echo off
echo PicX GUI Installer
echo ==================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set SHORTCUT_PATH=%USERPROFILE%\Desktop\PicX GUI.lnk

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT_PATH%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%main.py" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Installation completed!
echo You can now run PicX GUI from the desktop shortcut or by running:
echo   python main.py
echo.
pause
