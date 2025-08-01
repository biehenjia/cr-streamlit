cmake_minimum_required(VERSION 3.15)
project(pycr VERSION 0.1.0 LANGUAGES CXX)

# position‐independent code & C++20
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# default to Release (i.e. -O3) if no build type given
if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "No CMAKE_BUILD_TYPE specified; defaulting to Release")
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# global compiler flags: -O3 + CPU‐specific tuning in Release only
add_compile_options(
  $<$<CONFIG:Release>:-O3>
  $<$<CONFIG:Release>:-march=native>
)


add_compile_definitions(PYBIND11_DEBUG)

# fetch pybind11
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v3.0.0
)
FetchContent_MakeAvailable(pybind11)

# sources
file(GLOB CORE_SOURCES   "${CMAKE_CURRENT_LIST_DIR}/src/cpp_src/*.cpp")
file(GLOB BINDING_SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/cpp_bindings/*.cpp")

# core static lib
add_library(cr_core STATIC ${CORE_SOURCES})
target_include_directories(cr_core PUBLIC
  "${CMAKE_SOURCE_DIR}/src/cpp_include"
)

# pybind11 module
pybind11_add_module(pycr ${BINDING_SOURCES})
target_link_libraries(pycr
  PRIVATE
    cr_core
    pybind11::module
)
target_include_directories(pycr PRIVATE
  "${CMAKE_SOURCE_DIR}/src/cpp_include"
)

# output naming
if (WIN32)
  set_target_properties(pycr PROPERTIES
    OUTPUT_NAME "pycrlib" PREFIX "" SUFFIX ".pyd"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}"
  )
else()
  set_target_properties(pycr PROPERTIES
    OUTPUT_NAME "pycrlib" PREFIX "" SUFFIX ".so"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}"
  )
endif()
