cmake_minimum_required(VERSION 3.16)
project(gluon_innfos_readonly LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

get_filename_component(
  GLUON_REPOSITORY_ROOT
  "${CMAKE_CURRENT_SOURCE_DIR}/../../.."
  ABSOLUTE
)
set(
  INNFOS_SDK_ROOT
  "${GLUON_REPOSITORY_ROOT}/sdk/innfos-cpp-sdk/sdk"
  CACHE PATH
  "Path to the INNFOS C++ SDK root"
)
set(INNFOS_INCLUDE_DIR "${INNFOS_SDK_ROOT}/include")
set(INNFOS_LIBRARY "${INNFOS_SDK_ROOT}/lib/linux_x86_64/libActuatorController.so")

if(NOT EXISTS "${INNFOS_INCLUDE_DIR}/actuatorcontroller.h")
  message(FATAL_ERROR "INNFOS header not found: ${INNFOS_INCLUDE_DIR}/actuatorcontroller.h")
endif()
if(NOT EXISTS "${INNFOS_LIBRARY}")
  message(FATAL_ERROR "INNFOS library not found: ${INNFOS_LIBRARY}")
endif()

add_library(innfos_actuator_controller SHARED IMPORTED)
set_target_properties(
  innfos_actuator_controller
  PROPERTIES IMPORTED_LOCATION "${INNFOS_LIBRARY}"
)

add_executable(gluon_innfos_readonly_probe src/innfos_readonly_probe.cpp)
add_executable(gluon_innfos_safe_position_step src/innfos_safe_position_step.cpp)
add_executable(gluon_innfos_multi_joint_pose src/innfos_multi_joint_pose.cpp)
target_include_directories(
  gluon_innfos_readonly_probe
  PRIVATE "${INNFOS_INCLUDE_DIR}"
)
target_include_directories(
  gluon_innfos_safe_position_step
  PRIVATE "${INNFOS_INCLUDE_DIR}"
)
target_include_directories(
  gluon_innfos_multi_joint_pose
  PRIVATE "${INNFOS_INCLUDE_DIR}"
)
target_compile_definitions(
  gluon_innfos_readonly_probe
  PRIVATE ASIO_STANDALONE ASIO_HAS_STD_CHRONO
)
target_compile_definitions(
  gluon_innfos_safe_position_step
  PRIVATE ASIO_STANDALONE ASIO_HAS_STD_CHRONO
)
target_compile_definitions(
  gluon_innfos_multi_joint_pose
  PRIVATE ASIO_STANDALONE ASIO_HAS_STD_CHRONO
)
target_compile_options(gluon_innfos_readonly_probe PRIVATE -Wall -Wextra -Wpedantic)
target_compile_options(gluon_innfos_safe_position_step PRIVATE -Wall -Wextra -Wpedantic)
target_compile_options(gluon_innfos_multi_joint_pose PRIVATE -Wall -Wextra -Wpedantic)
target_link_libraries(
  gluon_innfos_readonly_probe
  PRIVATE innfos_actuator_controller pthread
)
target_link_libraries(
  gluon_innfos_safe_position_step
  PRIVATE innfos_actuator_controller pthread
)
target_link_libraries(
  gluon_innfos_multi_joint_pose
  PRIVATE innfos_actuator_controller pthread
)

# Allow a build-tree executable to locate the repository-provided SDK library
# without requiring a global ldconfig or LD_LIBRARY_PATH change.
set_target_properties(
  gluon_innfos_readonly_probe
  PROPERTIES BUILD_RPATH "${INNFOS_SDK_ROOT}/lib/linux_x86_64"
)
set_target_properties(
  gluon_innfos_safe_position_step
  PROPERTIES BUILD_RPATH "${INNFOS_SDK_ROOT}/lib/linux_x86_64"
)
set_target_properties(
  gluon_innfos_multi_joint_pose
  PROPERTIES BUILD_RPATH "${INNFOS_SDK_ROOT}/lib/linux_x86_64"
)
