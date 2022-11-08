cmake_minimum_required(VERSION 3.4.1)

project(lorentzian_test VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(Boost_USE_MULTITHREADED TRUE)
set(CMAKE_CXX_FLAGS "-I/usr/include/  -O2")
set(CMAKE_C_FLAGS "-I/usr/include/  -O2")

#Look for eigen and explicitly specify to use it. EIGEN3_INCLUDE_DIR Must be specified in the bashrc
include_directories( "$ENV{EIGEN3_INCLUDE_DIR}" "../TAMCMC-C-1.83.4/tamcmc/headers" "../TAMCMC-C-1.83.4/external/integrate" "../TAMCMC-C-1.83.4/test/lorentzian_test")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../)

#Bring the headers into the project
set(HEADERS  #_COMMON
    ../TAMCMC-C-1.83.4/tamcmc/headers/acoefs.h	
    ../TAMCMC-C-1.83.4/tamcmc/headers/build_lorentzian.h
    ../TAMCMC-C-1.83.4/tamcmc/headers/function_rot.h
    ../TAMCMC-C-1.83.4/external/integrate/activity.h
    ../TAMCMC-C-1.83.4/tamcmc/headers/linspace.h
   )

#Bring the core program sources into the project
set(SOURCES_MAIN  #_COMMON
    ../TAMCMC-C-1.83.4/test/lorentzian_test/lorentzian_test.cpp
    ../TAMCMC-C-1.83.4/tamcmc/sources/acoefs.cpp
    ../TAMCMC-C-1.83.4/tamcmc/sources/function_rot.cpp
    ../TAMCMC-C-1.83.4/tamcmc/sources/build_lorentzian.cpp
    ../TAMCMC-C-1.83.4/external/integrate/activity.cpp
    ../TAMCMC-C-1.83.4/tamcmc/sources/linspace.cpp
    )


find_package(Boost COMPONENTS system filesystem iostreams REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

add_executable(${CMAKE_PROJECT_NAME} ${HEADERS} ${SOURCES_MAIN})
target_link_libraries(${CMAKE_PROJECT_NAME})
