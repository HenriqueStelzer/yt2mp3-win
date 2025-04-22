@echo off
set "APP_DIR=C:\Users\%username%\yt2mp3-win"

if "%1"=="install" (
    pip install -r "%APP_DIR%\requirements.txt"
    winget install ffmpeg -e --id Gyan.FFmpeg
    echo doskey yt2mp3=python "%APP_DIR%\app.py" $* > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\yt2mp3_alias.bat"
    REG ADD "HKCU\Software\Microsoft\Command Processor" /v AutoRun /t REG_EXPAND_SZ /d "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\yt2mp3_alias.bat" /f   
    echo Installation completed.
    exit /b
)

if "%1"=="uninstall" (
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\yt2mp3_alias.bat"
    echo Uninstallation completed.
    rmdir /S /Q "%APP_DIR%"
    exit /b
)

echo Usage:
echo   install.bat install   - to install yt2mp3
echo   install.bat uninstall - to uninstall yt2mp3
