@echo off
setlocal

echo ==========
echo SSH Tunnel
echo ==========

:: User name for remote server
if "%~1"=="" (
    set /p SERVER_USER="Server user name: "
) else (
    set SERVER_USER=%~1
)
:: Host name for remote server
if "%~2"=="" (
    set /p SERVER_HOST="Server host or IP: "
) else (
    set SERVER_HOST=%~2
)

set SSHEXE=ssh

:loop
echo Starting SSH Tunnel to %SERVER_USER%@%SERVER_HOST% ...
%SSHEXE% -L 59000:localhost:5901 -C -N -l %SERVER_USER% %SERVER_HOST%

echo.
echo SSH connection lost. Retrying in 5 seconds...
timeout /t 5 /nobreak >nul
goto loop

pause
endlocal
