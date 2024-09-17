# GTK

## Environment

Windows 10+

GTK 4.x

MSYS2 UCRT64

CMake

## MSYS2

```bash
pacman -S mingw-w64-ucrt-x86_64-toolchain
pacman -S mingw-w64-ucrt-x86_64-gtk4

# find installed
pacman -Qi mingw-w64-ucrt-x86_64-gtk4

# get version if installed
pkg-config --modversion gtk4

# tree /f
│  CMakeLists.txt
├─build
└─src
        main.c

# /build
cmake ..

# build.ninja
ninja
```

