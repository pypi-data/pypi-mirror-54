cmake_minimum_required(VERSION 3.10)
project(pycascrel)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(PYCASCREL_USE_CONAN, "Use Conan to provide dependencies")

if(PYCASCREL_USE_CONAN)
	include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
	conan_basic_setup(NO_OUTPUT_DIRS)
else()
	find_package(spdlog REQUIRED)
	find_package(Eigen3 3.3 REQUIRED NO_MODULE)
endif()

find_package(pybind11 REQUIRED)

set(PYBIND11_CPP_STANDARD -std=c++11)

pybind11_add_module(
        pycascrel MODULE
        src/CascrelBinding.cpp
        src/CascadeCorrelationNetworkWrapper.cpp
        src/BuilderWrapper.cpp
        src/NormalInitializerParam.cpp
        src/DeltaRuleOptimizerParam.cpp
        src/HyperbolicTangentActivationParam.cpp
        src/LinearActivationParam.cpp
        src/SigmoidActivationParam.cpp
        src/SoftplusActivationParam.cpp
        src/MeanSquareLossParam.cpp
)

target_include_directories(pycascrel PRIVATE include)

if(PYCASCREL_USE_CONAN)
	target_link_libraries(pycascrel PRIVATE ${CONAN_LIBS})
else()
	target_link_libraries(pycascrel PRIVATE cascrel)
	target_link_libraries(pycascrel PRIVATE Eigen3::Eigen)
	target_link_libraries(pycascrel PRIVATE spdlog::spdlog)
endif()
