@echo off

set "ORIGINAL_PATH=%CD%"
set "PARENT_PATH=%ORIGINAL_PATH%\.."
:: Set the output file
set "OUTPUT_FILE=%ORIGINAL_PATH%\project-list.txt"

:: Delete the output file if it exists
if exist "%OUTPUT_FILE%" del "%OUTPUT_FILE%"

:: List all subdirectories except project-utility
for /d %%i in ("%PARENT_PATH%\*") do (
    if /i not "%%~nxi"=="project-utility" (
        setlocal enabledelayedexpansion
        rem Remove the unnecessary path prefix
        set "SUBDIR=%%~nxi"
        echo !SUBDIR!
        echo !SUBDIR! >> "%OUTPUT_FILE%"
        endlocal
    )
)

:: End
echo.
echo Done.

pause