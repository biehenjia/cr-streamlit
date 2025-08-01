cmake_minimum_required(VERSION 3.15)
project(pycr VERSION 0.1.0 LANGUAGES CXX)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD      20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
endif()
add_compile_definitions(PYBIND11_DEBUG)

include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v3.0.0
)
FetchContent_MakeAvailable(pybind11)

file(GLOB CORE_SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/cpp_src/*.cpp")

file(GLOB BINDING_SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/cpp_bindings/*.cpp")

add_library(cr_core STATIC ${CORE_SOURCES})
target_include_directories(cr_core PUBLIC
    "${CMAKE_SOURCE_DIR}/src/cpp_include"
)

pybind11_add_module(pycr ${BINDING_SOURCES})
target_link_libraries(pycr
  PRIVATE
    cr_core
    pybind11::module
)
target_include_directories(pycr PRIVATE
    "${CMAKE_SOURCE_DIR}/src/cpp_include"
)

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

