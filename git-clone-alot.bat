@echo off

set "originalPath=%CD%"
set "repoList=%originalPath%\git-clone-alot.txt"

cd ..

:: Check exist
if not exist "%repoList%" (
    echo Repository list file %repoList% not found.
    goto End
)

:: Read each line
for /F "tokens=*" %%G in ('type "%repoList%"') do (
    set "gitURL=%%G"
    setlocal enabledelayedexpansion
    :: Fetch the last of Git URL part for repo name
    for %%H in ("!gitURL!") do (
        set "repoName=%%~nH"
        set "repoPath=%%~dpH"
    )
    :: Check repo exist
    if not exist "!repoName!\" (
        echo Cloning !gitURL! into !repoName!
        git clone "!gitURL!"
    ) else (
        echo Repository !repoName! already exists.
    )
    endlocal
)

:End
cd "%originalPath%"
echo Done.

pause