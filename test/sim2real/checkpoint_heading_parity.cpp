// DESKTOP_DRY_RUN: stateful stdin fixture for the production C++ ObservationBuilder, including the wheel
// position error and the gyro heading error. Driven by test/sim2real/test_heading_parity.py.
#include <iomanip>
#include <iostream>
#include "tita_controller/adapter.hpp"

template<class T> void read(T & values) {for (auto & x : values) std::cin >> x;}

int main()
{
  using namespace tita;
  std::size_t count;
  std::cin >> count;
  std::vector<ObsElement> layout(count);
  for (auto & e : layout) std::cin >> e.kind >> e.index >> e.scale >> e.low >> e.high;
  Joints defaults{}, velocities{};
  read(defaults); read(velocities);
  WheelPositionConfig position;
  std::cin >> position.radius >> position.clip_m;
  read(position.zero_thresholds);
  HeadingConfig heading;
  std::cin >> heading.clip_rad >> heading.warmup_s >> heading.dt;
  read(heading.zero_thresholds);
  double bias;
  std::cin >> bias;
  ObservationBuilder builder(layout, defaults, velocities, position, heading);
  builder.set_gyro_bias(bias);
  int reset;
  std::cout << std::setprecision(17);
  while (std::cin >> reset) {
    RobotState s;
    std::array<double, 3> command{};
    std::vector<float> last(8);
    read(s.joint_pos); read(s.joint_vel); read(s.quat_wxyz); read(s.ang_vel); read(command); read(last);
    if (!std::cin) return 2;
    if (reset) builder.reset();
    for (auto x : builder.build(s, command, last)) std::cout << x << ' ';
    std::cout << '\n';
  }
}
