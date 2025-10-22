@echo off
color 0A
title Flaty

echo Demarrage de Flaty...
echo.

REM Vérifie la version de Python
python --version 2>nul | find "Python 3.14" >nul
if errorlevel 1 (
    echo ERREUR: Python 3.14 n'est pas detecte.
    echo Veuillez relancer install.bat pour corriger ce probleme.
    pause
    exit
)

REM Active l'environnement virtuel
call venv\Scripts\activate.bat

REM Lance l'application
python flaty.py

REM En cas d'erreur
if errorlevel 1 (
    color 0C
    echo.
    echo Une erreur est survenue...
    echo Si le probleme persiste, relancez 'install.bat'
    echo.
    pause
)