cmake_minimum_required(VERSION 3.20)
project(tray_winmain LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(tray_winmain WIN32
    main.cpp
)

target_link_libraries(tray_winmain PRIVATE user32 shell32)