// DESKTOP_DRY_RUN: pure-math replay executable; never links ROS/SDK or opens CAN.
#include <iomanip>
#include <iostream>
#include "tita_controller/state_machine.hpp"
int main()
{
  using namespace tita;
  Joints q{}, dq{}, previous{}, sample{}, velocity{};
  SitQuaternion imu{}, current_imu{};
  SitVector gyro{}, current_gyro{};
  double elapsed;
  const Joints limits{60., 60., 60., 12., 60., 60., 60., 12.};
  std::cout << std::setprecision(17);
  while (std::cin >> q[0]) {
    for (int i = 1; i < 8; ++i) std::cin >> q[i];
    for (auto * v : {&dq, &previous}) for (double & x : *v) std::cin >> x;
    for (double & x : imu) std::cin >> x;
    for (double & x : gyro) std::cin >> x;
    for (auto * v : {&sample, &velocity}) for (double & x : *v) std::cin >> x;
    for (double & x : current_imu) std::cin >> x;
    for (double & x : current_gyro) std::cin >> x;
    std::cin >> elapsed;
    if (!std::cin) return 2;
    SupportingSit controller;
    controller.start(q, dq, previous, imu, gyro);
    const auto torque = controller.torque(sample, velocity, elapsed, current_imu, current_gyro, limits);
    std::cout << sit_com_angle(sample, current_imu);
    for (double x : torque) std::cout << ' ' << x;
    std::cout << '\n';
  }
}
