cmake_minimum_required(VERSION 3.21.0)
project(hello_gtk4 VERSION 0.1.0)

# find GTK4 package
find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK4 REQUIRED gtk4)

link_directories(/ucrt64/lib)

add_executable(hello_gtk WIN32 src/main.c)

target_include_directories(hello_gtk PRIVATE ${GTK4_INCLUDE_DIRS})
target_link_libraries(hello_gtk ${GTK4_LIBRARIES})
target_compile_options(hello_gtk PRIVATE ${GTK4_CFLAGS_OTHER})

# auto copy .dll, for win
set(GTK_DLLS
    libepoxy-0.dll
    libgio-2.0-0.dll
    libglib-2.0-0.dll
    libcairo-script-interpreter-2.dll
    libgtk-4-1.dll
    #libgdk-4-1.dll
    #libpangowin32-1.0-0.dll
    #libharfbuzz-0.dll
    #libpango-1.0-0.dll
    #libgdk_pixbuf-2.0-0.dll
    #libcairo-gobject-2.dll
    #libcairo-2.dll
    libgraphene-1.0-0.dll
    #libgio-2.0-0.dll
    #libglib-2.0-0.dll
    #libintl-8.dll
    #libgobject-2.0-0.dll
    liblzo2-2.dll
)

function(find_msys2_root_from_compiler)
    if(CMAKE_C_COMPILER)
        get_filename_component(compilter_path "${CMAKE_C_COMPILER}" DIRECTORY)
        message(STATUS "C Compiler Path: ${compilter_path}")
        set(COMPILER_PATH "${compilter_path}" PARENT_SCOPE)
    endif()
endfunction()

find_msys2_root_from_compiler()
message(STATUS "COMPILER_PATH: ${COMPILER_PATH}")

foreach(DLL ${GTK_DLLS})
    add_custom_command(TARGET hello_gtk POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${COMPILER_PATH}/${DLL}" $<TARGET_FILE_DIR:hello_gtk>)
endforeach()