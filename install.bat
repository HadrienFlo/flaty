@echo off
color 0A
title Installation de Flaty

echo ========================================================
echo                 Installation de Flaty
echo ========================================================
echo.

REM Vérifie si Python est installé
python --version > nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERREUR: Python n'est pas installe sur votre ordinateur.
    echo.
    echo 1. Rendez-vous sur: https://www.python.org/downloads/windows/
    echo 2. Telechargez Python 3.12 (Download Windows installer 64-bit)
    echo 3. IMPORTANT: Lors de l'installation, cochez:
    echo    [X] Add Python to PATH
    echo    [X] Install launcher for all users
    echo.
    echo Une fois Python installe, relancez ce programme.
    echo.
    pause
    exit
)

REM Vérifie si Chrome est installé
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" > nul 2>&1
if errorlevel 1 (
    color 0E
    echo ATTENTION: Google Chrome n'est pas detecte sur votre systeme.
    echo Chrome est necessaire pour le bon fonctionnement de l'application.
    echo.
    echo Veuillez installer Chrome depuis: https://www.google.com/chrome/
    echo.
    pause
)

REM Crée un environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo Creation de l'environnement Python dedie...
    python -m venv venv
)

REM Active l'environnement virtuel
call venv\Scripts\activate.bat

REM Installe/Met à jour pip
python -m pip install --upgrade pip

REM Installe les dépendances
echo Installation des composants necessaires...
pip install -r requirements.txt

REM Crée un raccourci sur le bureau si inexistant
if not exist "%USERPROFILE%\Desktop\Flaty.lnk" (
    echo Creation du raccourci sur le bureau...
    powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Flaty.lnk'); $Shortcut.TargetPath = '%~dp0start.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
)

color 0A
echo.
echo ========================================================
echo            Installation terminee avec succes!
echo ========================================================
echo.
echo Pour lancer Flaty:
echo 1. Double-cliquez sur l'icone "Flaty" sur votre bureau
echo    OU
echo 2. Double-cliquez sur le fichier 'start.bat' dans ce dossier
echo.
echo L'application s'ouvrira dans votre navigateur par defaut.
echo.
pause