@echo off
set VPS_IP=178.128.59.217
set VPS_USER=root
set DEST_DIR=/root/filesaverbot

echo =========================================
echo Deploying FileSaverBot to %VPS_IP%...
echo =========================================

echo [1/3] Uploading client_secret.json...
scp client_secret.json %VPS_USER%@%VPS_IP%:%DEST_DIR%/

echo [2/3] Uploading templates...
scp -r templates %VPS_USER%@%VPS_IP%:%DEST_DIR%/

echo [3/3] Uploading python script (optional safety update)...
scp filesaver_bot.py %VPS_USER%@%VPS_IP%:%DEST_DIR%/

echo [4/4] Restarting service on VPS...
ssh %VPS_USER%@%VPS_IP% "systemctl restart filesaverbot"

echo.
echo =========================================
echo Deployment Completed!
echo =========================================
pause
