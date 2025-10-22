@echo off
color 0A
title Flaty

echo Demarrage de Flaty...
echo.

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