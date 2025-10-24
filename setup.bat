@echo off
color 0A
title Installation de Flaty

REM Vérifie si on est en mode administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :ADMIN
) else (
    color 0E
    echo Cette installation necessite des droits administrateur.
    echo Le programme va demander l'elevation des privileges...
    echo.
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit
)

:ADMIN
echo ========================================
echo     Configuration de l'environnement
echo ========================================
echo.

REM Configure la politique d'exécution PowerShell
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

REM Crée l'environnement virtuel
echo Creation de l'environnement Python...
python -m venv venv

REM Active l'environnement
echo Activation de l'environnement...
call venv\Scripts\activate.bat

REM Installe les dépendances
echo Installation des packages necessaires...
pip install -r requirements.txt

color 0A
echo.
echo ========================================
echo     Installation terminee avec succes
echo ========================================
echo.
echo Vous pouvez maintenant lancer l'application
echo avec la commande 'python flaty.py'
echo.
pause