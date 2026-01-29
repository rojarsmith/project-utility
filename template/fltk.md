# FLTK

## Msys2

```bash
pacman -Syu
pacman -S --needed \
  git \
  unzip \
  mingw-w64-ucrt-x86_64-toolchain \
  mingw-w64-ucrt-x86_64-cmake \
  mingw-w64-ucrt-x86_64-ninja \
  mingw-w64-ucrt-x86_64-zlib \
  mingw-w64-ucrt-x86_64-libpng \
  mingw-w64-ucrt-x86_64-libjpeg-turbo

FLTK_VER=1.4.4
echo $FLTK_VER

mkdir -p ~/fltk/src && cd ~/fltk/src
git clone https://github.com/fltk/fltk.git fltk
cd fltk
git checkout release-$FLTK_VER

# static libs
cmake -S . -B build-ucrt64-static -G Ninja \
  -D CMAKE_BUILD_TYPE=Debug \
  -D CMAKE_INSTALL_PREFIX=/opt/fltk-ucrt64-static

# Failure to disable FLTK_BUILD_TEST will result in incorrect LIB references, such as blocks, and only the compiled executable will be generated.
cmake -S . -B build-ucrt64-static -G Ninja \
  -D CMAKE_BUILD_TYPE=Debug \
  -D CMAKE_INSTALL_PREFIX=/opt/fltk-ucrt64-static \
  -DFLTK_BUILD_TEST=OFF

# shared libs
cmake -S . -B build-ucrt64 -G Ninja \
  -D CMAKE_BUILD_TYPE=Debug \
  -D CMAKE_INSTALL_PREFIX=/opt/fltk-ucrt64-shared \
  -D FLTK_BUILD_SHARED_LIBS=ON

cmake --build build-ucrt64-static
cmake --install build-ucrt64-static

find /opt/fltk-ucrt64-static -name "FLTKConfig.cmake" 2>/dev/null
ls -1 /opt/fltk-ucrt64-static/lib

mkdir -p ~/fltk/src/fltk-hello
cd ~/fltk/src/fltk-hello

cat > main.cpp <<'EOF'
#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Box.H>

static Fl_Box* g_text = nullptr;

static void on_click(Fl_Widget*, void*) {
    if (g_text) {
        g_text->label("Hello");
        g_text->redraw();
    }
}

int main() {
    Fl_Window win(360, 180, "FLTK Hello");

    Fl_Box text(20, 25, 320, 50, "");
    text.labelsize(28);
    g_text = &text;

    Fl_Button btn(130, 100, 100, 40, "Press");
    btn.callback(on_click);

    win.end();
    win.show();
    return Fl::run();
}
EOF

cat > CMakeLists.txt <<'EOF'
cmake_minimum_required(VERSION 3.20)
project(fltk_hello_button LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(FLTK CONFIG REQUIRED)

add_executable(fltk_hello main.cpp)
target_link_libraries(fltk_hello PRIVATE fltk::fltk)
EOF

cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_PREFIX_PATH="/opt/fltk-ucrt64-static"
  
cmake --build build
./build/fltk_hello.exe

#clean
rm -rf ~/fltk
rm -rf /opt/fltk-ucrt64-static
```

