cmake_minimum_required(VERSION 3.14)
project(tita_stage1_controller)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(controller_interface REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(realtime_tools REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(OpenSSL REQUIRED)

include(FetchContent)
set(ONNXRUNTIME_VERSION "1.19.2")
if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|arm64)$")
  set(ONNXRUNTIME_ARCHIVE "onnxruntime-linux-aarch64-${ONNXRUNTIME_VERSION}")
  set(ONNXRUNTIME_URL "https://github.com/microsoft/onnxruntime/releases/download/v${ONNXRUNTIME_VERSION}/${ONNXRUNTIME_ARCHIVE}.tgz")
  set(ONNXRUNTIME_SHA256 "5e30145277d6d6fcb0e8f14f0d0ab5048af7b13ffd608023bb1e2875621fab07")
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|amd64)$")
  set(ONNXRUNTIME_ARCHIVE "onnxruntime-linux-x64-${ONNXRUNTIME_VERSION}")
  set(ONNXRUNTIME_URL "https://github.com/microsoft/onnxruntime/releases/download/v${ONNXRUNTIME_VERSION}/${ONNXRUNTIME_ARCHIVE}.tgz")
  set(ONNXRUNTIME_SHA256 "eb00c64e0041f719913c4080e0fed7d9963dc3aa9b54664df6036d8308dbcd33")
else()
  message(FATAL_ERROR "Unsupported ONNX Runtime architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()
FetchContent_Declare(onnxruntime_prebuilt
  URL "${ONNXRUNTIME_URL}"
  URL_HASH "SHA256=${ONNXRUNTIME_SHA256}")
FetchContent_GetProperties(onnxruntime_prebuilt)
if(NOT onnxruntime_prebuilt_POPULATED)
  FetchContent_Populate(onnxruntime_prebuilt)
endif()
set(ONNXRUNTIME_ROOT "${onnxruntime_prebuilt_SOURCE_DIR}")
add_library(onnxruntime SHARED IMPORTED)
set_target_properties(onnxruntime PROPERTIES
  IMPORTED_LOCATION "${ONNXRUNTIME_ROOT}/lib/libonnxruntime.so.1.19.2"
  INTERFACE_INCLUDE_DIRECTORIES "${ONNXRUNTIME_ROOT}/include")

add_library(${PROJECT_NAME} SHARED
  src/stage1_core.cpp
  src/rl_pipeline.cpp
  src/stage1_controller.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(${PROJECT_NAME}
  controller_interface hardware_interface pluginlib rclcpp rclcpp_lifecycle realtime_tools
  sensor_msgs std_msgs std_srvs)
target_link_libraries(${PROJECT_NAME} onnxruntime OpenSSL::Crypto)
set_target_properties(${PROJECT_NAME} PROPERTIES INSTALL_RPATH "$ORIGIN")
pluginlib_export_plugin_description_file(controller_interface tita_stage1_controller_plugin.xml)

install(TARGETS ${PROJECT_NAME} EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib LIBRARY DESTINATION lib RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
install(DIRECTORY config launch DESTINATION share/${PROJECT_NAME})
install(FILES
  "${ONNXRUNTIME_ROOT}/lib/libonnxruntime.so"
  "${ONNXRUNTIME_ROOT}/lib/libonnxruntime.so.1"
  "${ONNXRUNTIME_ROOT}/lib/libonnxruntime.so.1.19.2"
  "${ONNXRUNTIME_ROOT}/lib/libonnxruntime_providers_shared.so"
  DESTINATION lib)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_stage1_core test/test_stage1_core.cpp src/stage1_core.cpp)
  target_include_directories(test_stage1_core PRIVATE include)
  ament_add_gtest(test_rl_pipeline test/test_rl_pipeline.cpp src/rl_pipeline.cpp)
  target_include_directories(test_rl_pipeline PRIVATE include "${ONNXRUNTIME_ROOT}/include")
  target_link_libraries(test_rl_pipeline onnxruntime OpenSSL::Crypto)
  get_filename_component(TITA_REPOSITORY_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../.." ABSOLUTE)
  if(EXISTS "${TITA_REPOSITORY_ROOT}/deploy/tita/policy.onnx")
    set(TITA_TEST_POLICY_PATH "${TITA_REPOSITORY_ROOT}/deploy/tita/policy.onnx")
  elseif(EXISTS "/home/robot/tita_ws/policy/policy.onnx")
    set(TITA_TEST_POLICY_PATH "/home/robot/tita_ws/policy/policy.onnx")
  elseif(EXISTS "/home/robot/tita_policy/policy.onnx")
    set(TITA_TEST_POLICY_PATH "/home/robot/tita_policy/policy.onnx")
  endif()
  if(TITA_TEST_POLICY_PATH)
    target_compile_definitions(test_rl_pipeline PRIVATE
      TITA_TEST_POLICY_PATH="${TITA_TEST_POLICY_PATH}")
  endif()
  set(TITA_TEST_DIAGNOSTIC_POLICY_PATH
    "${TITA_REPOSITORY_ROOT}/deploy/tita/policy_my26_1700_estimator_diagnostic.onnx")
  if(NOT EXISTS "${TITA_TEST_DIAGNOSTIC_POLICY_PATH}" AND
    EXISTS "/home/robot/tita_ws/policy/policy_estimator_diagnostic.onnx")
    set(TITA_TEST_DIAGNOSTIC_POLICY_PATH
      "/home/robot/tita_ws/policy/policy_estimator_diagnostic.onnx")
  endif()
  if(EXISTS "${TITA_TEST_DIAGNOSTIC_POLICY_PATH}")
    target_compile_definitions(test_rl_pipeline PRIVATE
      TITA_TEST_DIAGNOSTIC_POLICY_PATH="${TITA_TEST_DIAGNOSTIC_POLICY_PATH}")
  endif()
  ament_add_gtest(test_controller_plugin test/test_controller_plugin.cpp)
  ament_target_dependencies(test_controller_plugin controller_interface pluginlib rclcpp)
  if(EXISTS "${TITA_TEST_DIAGNOSTIC_POLICY_PATH}")
    target_compile_definitions(test_controller_plugin PRIVATE
      TITA_TEST_CONTROLLER_POLICY_PATH="${TITA_TEST_DIAGNOSTIC_POLICY_PATH}")
  endif()
endif()

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(controller_interface hardware_interface pluginlib rclcpp realtime_tools sensor_msgs std_srvs)
ament_package()
