cmake_minimum_required(VERSION 3.16)
project(raytracing)

set(CMAKE_CXX_STANDARD 14)

# add extra include directories
include_directories(/usr/local/include)

# add extra lib directories
link_directories(/usr/local/lib)

add_executable(raytracing
        main.cpp
        vectors.h
        window.h
        util.h)

# OpenGL
find_package(OpenGL REQUIRED)

# GLM
#find_package(GLM REQUIRED)
#message(STATUS "GLM included at ${GLM_INCLUDE_DIR}")

# GLFW
find_package(GLFW3 REQUIRED)
message(STATUS "Found GLFW3 in ${GLFW3_INCLUDE_DIR}")

# GLEW
find_package(GLEW REQUIRED)
message(STATUS "Found GLEW in ${GLEW_INCLUDE_DIR}")

target_link_libraries(raytracing glfw)
target_link_libraries(raytracing GLEW)

# mac, it's important to take this step
if (APPLE)
    target_link_libraries(raytracing "-framework OpenGL")
endif()
