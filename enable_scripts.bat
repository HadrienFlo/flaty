@echo off
color 0E
title Configuration PowerShell

echo ================================================
echo     Configuration de la politique d'execution
echo ================================================
echo.
echo Ce script va autoriser l'execution des scripts
echo PowerShell sur votre systeme.
echo.
echo Une fenetre d'elevation des privileges va s'ouvrir.
echo Veuillez accepter pour continuer.
echo.
pause

REM Crée un script PowerShell temporaire
echo Set-ExecutionPolicy RemoteSigned -Force > "%TEMP%\EnableScripts.ps1"
echo Write-Host "Configuration terminee avec succes!" >> "%TEMP%\EnableScripts.ps1"
echo pause >> "%TEMP%\EnableScripts.ps1"

REM Exécute PowerShell avec les privilèges administrateur
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%TEMP%\EnableScripts.ps1\"' -Verb RunAs"

echo.
echo Une fois la configuration terminee, vous pouvez
echo lancer le script 'install.bat'
echo.
pause