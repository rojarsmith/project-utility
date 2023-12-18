REM Set up compiler
CALL "C:\Qt\Tools\mingw1120_64\bin\g++.exe" -v
SET _ROOT=C:\Qt\6.5.3\Src
SET _TOOL=C:\Qt\Tools\mingw1120_64\bin;C:\Qt\Tools\Ninja
SET PATH=%_TOOL%;%_ROOT%;%PATH%
SET _ROOT=
SET _TOOL=
cmd