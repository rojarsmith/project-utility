cmake_minimum_required(VERSION 4.0.1)
project(hello_gtk4 VERSION 0.1.0)



# find GTK4 package
find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK4 REQUIRED gtk4)

# Add executable
add_executable(hello_gtk WIN32 src/main.c)

# Link GTK4 libraries and set include directories
target_include_directories(hello_gtk PRIVATE ${GTK4_INCLUDE_DIRS})
target_link_libraries(hello_gtk ${GTK4_LIBRARIES})
target_compile_options(hello_gtk PRIVATE ${GTK4_CFLAGS_OTHER})
message(STATUS "${GTK4_LIBRARIES}")

# message("$ENV{MSYS2_ROOT}/ucrt64/bin")
link_directories(/ucrt64/lib)
# Find MSYS2 installation path automatically
set(MSYS2_BIN_PATH /ucrt64/lib)
message(STATUS ${MSYS2_BIN_PATH})
message(STATUS ${MSYS2_BIN_PATH})
message(STATUS ${MSYS2_ROOT})

# auto copy .dll, for win
set(GTK_DLLS
    # libepoxy-0.dll
    # libgio-2.0-0.dll
    # libglib-2.0-0.dll
    libcairo-script-interpreter-2.dll
    libgtk-4-1.dll
    # libgdk-4-1.dll
    # libpangowin32-1.0-0.dll
    # libharfbuzz-0.dll
    libpango-1.0-0.dll
    # libgdk_pixbuf-2.0-0.dll
    # libcairo-gobject-2.dll
    # libcairo-2.dll
    libgraphene-1.0-0.dll
    libgio-2.0-0.dll
    libglib-2.0-0.dll
    # libintl-8.dll
    # libgobject-2.0-0.dll
    # liblzo2-2.dll
    libpng16-16.dll
    libgstallocators-1.0-0.dll
    libgstd3d12-1.0-0.dll
    libgstallocators-1.0-0.dll
    libgstplay-1.0-0.dll
    libgstreamer-1.0-0.dll
    libgstgl-1.0-0.dll
    libgstvideo-1.0-0.dll
    libharfbuzz-subset-0.dll
    libjpeg-8.dll
    libtiff-6.dll
    libgstd3dshader-1.0-0.dll
    libgstbase-1.0-0.dll
    libgstpbutils-1.0-0.dll
    liborc-0.4-0.dll
    libgsttag-1.0-0.dll
    libjbig-0.dll
    libLerc.dll
    libdeflate.dll
    libwebp-7.dll
    libgstaudio-1.0-0.dll
    libsharpyuv-0.dll
    libstdc++-6.dll
    libwinpthread-1.dll
    libharfbuzz-0.dll
)

foreach(DLL ${GTK_DLLS})
    add_custom_command(TARGET hello_gtk POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "C:/msys64/ucrt64/bin/${DLL}" $<TARGET_FILE_DIR:hello_gtk>)
endforeach()
