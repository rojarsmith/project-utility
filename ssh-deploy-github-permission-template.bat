@echo off
setlocal

set USER=
set HOST=
set BOOK=ssh-deploy-github-permission.sh
set SUDO_PASS=
set GITHUB_USER=
set GITHUB_REPO=
set DEPLOY_KEY_TITLE=
set GITHUB_TOKEN=
@REM Infinite loop
@REM set KEY_FILE=/root/.ssh/id_rsa
@REM set SSH_CONFIG_FILE=/root/.ssh/config

call ssh-deploy.bat %USER% %HOST% %BOOK% %SUDO_PASS% %GITHUB_USER% %GITHUB_REPO% %DEPLOY_KEY_TITLE% %GITHUB_TOKEN%
@REM call ssh-deploy.bat %USER% %HOST% %BOOK% %SUDO_PASS% %GITHUB_USER% %GITHUB_REPO% %DEPLOY_KEY_TITLE% %GITHUB_TOKEN% %KEY_FILE% %SSH_CONFIG_FILE%

endlocal
