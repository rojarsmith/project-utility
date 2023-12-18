# Qt Env

## Windows

MSYS2 MINGW64

```bash
# Search package
pacman -Ss mingw-w64-x86_64-qt6
pacman -Ss mingw-w64-harfbuzz-

pacman -S --needed mingw-w64-x86_64-qt6-static mingw-w64-x86_64-qt-creator mingw-w64-x86_64-clang mingw-w64-x86_64-gdb mingw-w64-x86_64-cmake

# More dll lack
pacman -S --needed mingw-w64-x86_64-editorconfig-qtcreator
pacman -S --needed mingw-w64-x86_64-qt-creator-devel
```

CMake

```shell
# GCC
configure.bat -debug -static -static-runtime -confirm-license -opensource -platform win32-g++ -nomake examples -prefix "C:\temp\qt-6.5.3-static-mingw_64-debug" -j 8

# VS
configure.bat -static -prefix "C:\Qt-6.5.3-static" -confirm-license -opensource  -debug-and-release -platform win32-msvc  -nomake examples -nomake tests  -plugin-sql-sqlite -plugin-sql-odbc -qt-zlib -qt-libpng -qt-libjpeg -opengl desktop -mp
```

Compile

```shell
cmake --build . --parallel
cmake --install .
```

Fix MINGW64 Qt6 static link problems.

```cmake
if(QT_FEATURE_static STREQUAL "ON" AND WIN32 AND MINGW)
    set_property(TARGET harfbuzz::harfbuzz PROPERTY
    IMPORTED_IMPLIB ${harfbuzz_DIR}../../../libharfbuzz.dll.a)
endif()
```

