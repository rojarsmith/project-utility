@echo off

set "originalPath=%CD%"

cd ..

for /r %%d in (.) do (
    if exist "%%d\.git" (
        echo Found .git in %%d
        pushd "%%d"
        git pull
        popd
    )
)

cd %originalPath%

echo Done.

pause