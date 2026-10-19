cmake_minimum_required(VERSION 3.8)
project(tita_gluon_urdf)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/generate_combined_urdf.py
    scripts/generate_tita_gluon_2l6_4l3_urdf.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
