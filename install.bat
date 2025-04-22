@echo off
set "yt2mp3-win"

if "%1"=="install" (
    if not exist "%APP_DIR%" mkdir "%APP_DIR%"
    xcopy /E /I /Y "..\yt2mp3" "%APP_DIR%"
    pip install -r "%APP_DIR%\requirements.txt"
    winget install ffmpeg -e --id Gyan.FFmpeg
    echo doskey yt2mp3=python "%APP_DIR%\app.py" $* > "%USERPROFILE%\yt2mp3_alias.bat"
    echo Installation completed.
    exit /b
)

if "%1"=="uninstall" (
    rmdir /S /Q "%APP_DIR%"
    del "%USERPROFILE%\yt2mp3_alias.bat"
    echo Uninstallation completed.
    exit /b
)

echo Usage:
echo   install.bat install   - to install yt2mp3
echo   install.bat uninstall - to uninstall yt2mp3
