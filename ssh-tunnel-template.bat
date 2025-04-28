@echo off
setlocal

:: If the execution console leaves the focus, 
:: it may get stuck in the middle and require enter to continue execution.

:: User name for remote server
set SERVER_USER=
:: Host name for remote server
set SERVER_HOST=

call ssh-tunnel.bat %SERVER_USER% %SERVER_HOST%

endlocal
