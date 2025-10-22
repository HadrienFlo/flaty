@echo off
color 0A
title Installation de Flaty

echo ========================================================
echo                 Installation de Flaty
echo ========================================================
echo.

REM Vérifie si Python est installé (plusieurs méthodes)
set PYTHON_FOUND=0

REM Teste la commande python
python --version 2>nul | find "Python 3.14" >nul
if not errorlevel 1 set PYTHON_FOUND=1

REM Teste la commande py
if %PYTHON_FOUND%==0 (
    py -3.14 --version 2>nul
    if not errorlevel 1 set PYTHON_FOUND=1
)

REM Cherche Python dans les emplacements courants
if %PYTHON_FOUND%==0 (
    if exist "C:\Program Files\Python314\python.exe" set PYTHON_FOUND=2
    if exist "C:\Program Files (x86)\Python314\python.exe" set PYTHON_FOUND=2
    if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" set PYTHON_FOUND=2
)

if %PYTHON_FOUND%==0 (
    color 0C
    echo ERREUR: Python n'est pas installe sur votre ordinateur.
    echo.
    echo 1. Rendez-vous sur: https://www.python.org/downloads/windows/
    echo 2. Telechargez Python 3.14 (Download Windows installer 64-bit)
    echo 3. IMPORTANT: Lors de l'installation, cochez:
    echo    [X] Add Python to PATH
    echo    [X] Install launcher for all users
    echo.
    echo Une fois Python installe, relancez ce programme.
    echo.
    pause
    exit
)

if %PYTHON_FOUND%==2 (
    color 0E
    echo Python est installe mais n'est pas accessible dans le PATH.
    echo.
    echo Solutions possibles:
    echo 1. Relancez l'installation de Python et cochez "Add Python to PATH"
    echo    OU
    echo 2. Ajoutez manuellement Python au PATH:
    echo    a. Appuyez sur Windows + R
    echo    b. Tapez "sysdm.cpl" et appuyez sur Enter
    echo    c. Allez dans l'onglet "Avance"
    echo    d. Cliquez sur "Variables d'environnement"
    echo    e. Dans "Variables systeme", selectionnez "Path"
    echo    f. Cliquez sur "Modifier"
    echo    g. Ajoutez le chemin vers Python (ex: C:\Program Files\Python314)
    echo    h. Ajoutez aussi le chemin vers les Scripts (ex: C:\Program Files\Python314\Scripts)
    echo    i. Cliquez OK partout
    echo    j. Redemarrez votre ordinateur
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