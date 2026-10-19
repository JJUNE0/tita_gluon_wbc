cmake_minimum_required(VERSION 3.14)
project(tita_controller)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_options(-Wall -Wextra -O2)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tita_robot REQUIRED)
find_package(Eigen3 REQUIRED)

# Prebuilt ONNX Runtime for the build machine (x86_64 desktop or aarch64 robot).
include(FetchContent)
set(ORT_VERSION 1.19.2)
if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|arm64)$")
  set(ORT_NAME onnxruntime-linux-aarch64-${ORT_VERSION})
else()
  set(ORT_NAME onnxruntime-linux-x64-${ORT_VERSION})
endif()
FetchContent_Declare(onnxruntime
  URL https://github.com/microsoft/onnxruntime/releases/download/v${ORT_VERSION}/${ORT_NAME}.tgz)
FetchContent_MakeAvailable(onnxruntime)
set(ORT_DIR ${onnxruntime_SOURCE_DIR})

add_executable(tita_node src/tita_node.cpp)
target_include_directories(tita_node PRIVATE include ${ORT_DIR}/include)
target_link_directories(tita_node PRIVATE ${ORT_DIR}/lib)
target_link_libraries(tita_node onnxruntime ${tita_robot_LIBRARIES} Eigen3::Eigen)
ament_target_dependencies(tita_node rclcpp sensor_msgs std_msgs tita_robot)
set_target_properties(tita_node PROPERTIES INSTALL_RPATH "$ORIGIN/../../lib")

install(TARGETS tita_node DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS ${CMAKE_CURRENT_SOURCE_DIR}/../../run_flashsac.sh DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY policies DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(DIRECTORY ${ORT_DIR}/lib/ DESTINATION lib FILES_MATCHING PATTERN "libonnxruntime.so*")

ament_environment_hooks(env/flashsac_logs.sh.in)
ament_package()
