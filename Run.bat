@echo off
chcp 65001 > nul

setlocal enabledelayedexpansion
set "script=%~dp0Youtube_live_Auto_yt-dlp.py"

title Youtube 直播自動下載器 ver 1.1 by.鮪魚大師

python "!script!"
PAUSE
