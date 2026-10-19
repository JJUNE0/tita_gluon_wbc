cmake_minimum_required(VERSION 3.8)
project(gluon_2l6_4l3_urdf)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch meshes rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/generate_urdf.py scripts/audit_inertials.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
