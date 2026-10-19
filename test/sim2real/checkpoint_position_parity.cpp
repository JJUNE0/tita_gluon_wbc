// DESKTOP_DRY_RUN: stdin fixtures exercise production C++ observation/filter/PD code only.
#include <iomanip>
#include <iostream>
#include "tita_controller/adapter.hpp"
#include "tita_controller/leg_action_filter.hpp"

template<class T> void read(T & values) {for (auto & x : values) std::cin >> x;}
template<class T> void print(const T & values) {for (auto x : values) std::cout << x << ' ';}

int main()
{
  using namespace tita;
  std::size_t count;
  std::cin >> count;
  std::vector<ObsElement> layout(count);
  for (auto & e : layout) std::cin >> e.kind >> e.index >> e.scale >> e.low >> e.high;
  Joints defaults{}, velocities{}, kp{}, kd{}, limit{};
  read(defaults); read(velocities); read(kp); read(kd); read(limit);
  std::vector<ActionTerm> terms(8);
  std::vector<int64_t> order;
  for (auto & t : terms) {
    std::cin >> t.joint >> t.velocity >> t.scale >> t.offset >> t.low >> t.high;
    order.push_back(t.joint);
  }
  WheelPositionConfig position;
  std::cin >> position.radius >> position.clip_m;
  read(position.zero_thresholds);
  std::string mode;
  std::cin >> mode;
  ObservationBuilder builder(layout, defaults, velocities, position);
  LegActionFilter filter(mode, order);
  ActionAdapter adapter(terms, kp, kd, limit);
  int reset;
  std::cout << std::setprecision(17);
  while (std::cin >> reset) {
    RobotState s;
    std::array<double, 3> command{};
    std::vector<float> last(8), action(8);
    read(s.joint_pos); read(s.joint_vel); read(s.quat_wxyz); read(s.ang_vel);
    read(command); read(last); read(action);
    if (!std::cin) return 2;
    if (reset) {builder.reset(); filter.reset();}
    const auto obs = builder.build(s, command, last);
    const auto applied = filter.update(action);
    print(obs); print(applied); print(adapter.compute(applied, s.joint_pos, s.joint_vel));
    std::cout << '\n';
  }
}
