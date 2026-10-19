// DESKTOP_DRY_RUN: pure math executable, no ROS/CAN/SDK.
#include <iomanip>
#include <iostream>
#include <string>
#include "tita_controller/velocity_bias.hpp"

template<class T> void read(T & values) {for (auto & value : values) std::cin >> value;}

int main(int argc, char ** argv)
{
  std::cout << std::setprecision(17);
  if (argc != 2) return 2;
  if (std::string(argv[1]) == "law") {
    double limit, slew, sign;
    std::cin >> limit >> slew >> sign;
    tita::VelocityBiasLaw law(limit, slew, sign);
    double velocity, dt;
    int enabled;
    while (std::cin >> velocity >> dt >> enabled) {
      law.update(velocity, dt, enabled != 0);
      std::cout << law.filtered << ' ' << law.integral << ' ' << law.bias << ' '
                << law.age << '\n';
    }
    return 0;
  }
  const bool status = std::string(argv[1]) == "status";
  const bool enabled = std::string(argv[1]) == "on" || status;
  std::vector<double> xyz(24), rpy(24), axes(24);
  read(xyz); read(rpy); read(axes);
  double radius, sign;
  std::cin >> radius >> sign;
  tita::Joints kp{}, kd{}, limit{};
  read(kp); read(kd); read(limit);
  std::vector<tita::ActionTerm> terms(8);
  for (auto & term : terms) {
    std::cin >> term.joint >> term.velocity >> term.scale >> term.offset >> term.low >> term.high;
  }
  tita::WheelVelocityBias hold(xyz, rpy, axes, radius, sign, {kd[3], kd[7]});
  tita::ActionAdapter adapter(terms, kp, kd, limit);
  int rl;
  double dt;
  while (std::cin >> rl >> dt) {
    std::array<double, 3> command{};
    tita::RobotState s;
    std::vector<float> action(8);
    read(command); read(s.joint_pos); read(s.joint_vel); read(s.quat_wxyz); read(s.ang_vel); read(action);
    if (enabled && rl != 0) hold.update(s, command, dt);
    else hold.reset();
    const auto baseline = adapter.compute(action, s.joint_pos, s.joint_vel);
    const auto actual = adapter.compute(action, s.joint_pos, s.joint_vel, hold.wheel_offsets());
    for (float value : hold.diagnostics()) std::cout << value << ' ';
    for (double value : actual) std::cout << value << ' ';
    for (double value : baseline) std::cout << value << ' ';
    if (status) std::cout << hold.acquired() << ' ' << hold.inhibited() << ' '
                          << hold.estimated_drift() << ' ' << hold.pitch_reference();
    std::cout << '\n';
  }
}
