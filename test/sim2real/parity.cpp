// DESKTOP_DRY_RUN: run sim2real adapter/state machine on a fixture written by test_sim2real_parity.py.
// Prints C++ observations, torques and states, one line per sample.
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

#include "tita_controller/adapter.hpp"
#include "tita_controller/state_machine.hpp"

using namespace tita;

std::map<std::string, std::vector<double>> load(const char * path)
{
  std::map<std::string, std::vector<double>> data;
  std::ifstream file(path);
  std::string line, key;
  while (std::getline(file, line)) {
    std::istringstream in(line);
    in >> key;
    double value;
    while (in >> value) data[key].push_back(value);
  }
  return data;
}

Joints joints(const std::vector<double> & v, std::size_t offset = 0)
{
  Joints j{};
  for (std::size_t i = 0; i < 8; ++i) j[i] = v[offset + i];
  return j;
}

template<class T>
void print(const char * tag, const T & values)
{
  std::cout << tag;
  for (double v : values) std::cout << ' ' << v;
  std::cout << '\n';
}

int main(int, char ** argv)
{
  auto d = load(argv[1]);
  std::vector<ObsElement> layout;
  for (std::size_t i = 0; i < d["obs_kind"].size(); ++i) {
    layout.push_back({int(d["obs_kind"][i]), int(d["obs_index"][i]), d["obs_scale"][i], d["obs_low"][i], d["obs_high"][i]});
  }
  std::vector<ActionTerm> terms;
  for (std::size_t i = 0; i < d["action_joint"].size(); ++i) {
    terms.push_back({int(d["action_joint"][i]), d["action_velocity"][i] > .5, d["action_scale"][i],
      d["action_offset"][i], d["action_low"][i], d["action_high"][i]});
  }
  WheelPositionConfig position;
  if (d.count("wheel_position_radius")) {
    position.radius = d["wheel_position_radius"][0];
    position.clip_m = d["wheel_position_clip_m"][0];
    std::copy_n(d["wheel_position_zero_thresholds"].begin(), 3, position.zero_thresholds.begin());
  }
  ObservationBuilder obs_builder(layout, joints(d["default_joint_angles"]), joints(d["default_joint_velocities"]), position);
  ActionAdapter adapter(terms, joints(d["joint_kp"]), joints(d["joint_kd"]), joints(d["torque_limit"]));
  std::cout.precision(9);
  const std::size_t samples = d["q"].size() / 8;
  for (std::size_t n = 0; n < samples; ++n) {
    RobotState s;
    s.joint_pos = joints(d["q"], 8 * n);
    s.joint_vel = joints(d["dq"], 8 * n);
    s.quat_wxyz = {d["quat"][4 * n], d["quat"][4 * n + 1], d["quat"][4 * n + 2], d["quat"][4 * n + 3]};
    s.ang_vel = {d["gyro"][3 * n], d["gyro"][3 * n + 1], d["gyro"][3 * n + 2]};
    const std::array<double, 3> command{d["cmd"][3 * n], d["cmd"][3 * n + 1], d["cmd"][3 * n + 2]};
    const std::vector<float> last(d["last"].begin() + 8 * n, d["last"].begin() + 8 * n + 8);
    const std::vector<float> action(d["action"].begin() + 8 * n, d["action"].begin() + 8 * n + 8);
    print("obs", obs_builder.build(s, command, last));
    print("torque", adapter.compute(action, s.joint_pos, s.joint_vel));
  }
  StateMachine sm(joints(d["torque_limit"]));
  sm.request(State::TransformUp, joints(d["sm_start"]));
  const std::size_t steps = d["sm_q"].size() / 8;
  for (std::size_t n = 0; n < steps; ++n) {
    sm.update(d["sm_dt"][0]);
    print("sm_torque", sm.torque(joints(d["sm_q"], 8 * n), joints(d["sm_dq"], 8 * n)));
    std::cout << "sm_state " << (sm.state() == State::Sit ? 1 : 0) << '\n';
  }
}
