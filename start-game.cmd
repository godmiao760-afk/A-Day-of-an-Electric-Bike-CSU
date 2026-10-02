@echo off
cd /d "%~dp0"
python start_game.py %*
if errorlevel 1 pause
