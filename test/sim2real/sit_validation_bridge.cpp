// VALIDATION_SIM: native sim2real math only; no robot SDK, ROS or CAN linkage.
#include <algorithm>
#include <memory>
#include <string>
#include "tita_controller/adapter.hpp"

namespace
{
tita::Joints joints(const double * values)
{
  tita::Joints result{};
  std::copy(values, values + 8, result.begin());
  return result;
}
struct Bridge
{
  tita::StateMachine sm;
  tita::ActionAdapter adapter;
  tita::ObservationBuilder observer;
  Bridge(const double * p, std::vector<tita::ActionTerm> actions,
    std::vector<tita::ObsElement> observations)
  : sm(joints(p)), adapter(std::move(actions), joints(p+24), joints(p+32), joints(p)),
    observer(std::move(observations), joints(p+8), joints(p+16)) {}
};
std::string error;
}

extern "C"
{
void * sit_create(const double * p)
{
  try {
    std::vector<tita::ActionTerm> actions;
    std::vector<tita::ObsElement> observations;
    for (int i = 0; i < 8; ++i) {
      const double * a = p + 40 + 6*i;
      actions.push_back({static_cast<int>(a[0]), a[1] != 0., a[2], a[3], a[4], a[5]});
    }
    const int count = static_cast<int>(p[88]);
    for (int i = 0; i < count; ++i) {
      const double * a = p + 89 + 5*i;
      observations.push_back({static_cast<int>(a[0]), static_cast<int>(a[1]), a[2], a[3], a[4]});
    }
    return new Bridge(p, actions, observations);
  } catch (const std::exception & e) {error = e.what(); return nullptr;}
}
const char * sit_error() {return error.c_str();}
void sit_destroy(void * handle) {delete static_cast<Bridge *>(handle);}
int sit_request(void * handle, int state, const double * q, const double * previous)
{
  return static_cast<Bridge *>(handle)->sm.request(static_cast<tita::State>(state), joints(q), joints(previous));
}
void sit_sensors(void * handle, const double * q, const double * dq, const double * imu,
  const double * gyro, int valid)
{
  tita::SitQuaternion quat{}; tita::SitVector rate{};
  std::copy(imu, imu+4, quat.begin()); std::copy(gyro, gyro+3, rate.begin());
  static_cast<Bridge *>(handle)->sm.observe(joints(q), joints(dq), quat, rate, valid != 0);
}
double sit_angle(const double * q, const double * imu)
{
  tita::SitQuaternion quat{}; std::copy(imu, imu+4, quat.begin());
  return tita::sit_com_angle(joints(q), quat);
}
void sit_update(void * handle, double dt) {static_cast<Bridge *>(handle)->sm.update(dt);}
int sit_state(void * handle) {return static_cast<int>(static_cast<Bridge *>(handle)->sm.state());}
void sit_torque(void * handle, const double * q, const double * dq, double * output)
{
  const auto tau = static_cast<Bridge *>(handle)->sm.torque(joints(q), joints(dq));
  std::copy(tau.begin(), tau.end(), output);
}
void sit_action(void * handle, const double * action, const double * q, const double * dq, double * output)
{
  const std::vector<float> raw(action, action+8);
  const auto tau = static_cast<Bridge *>(handle)->adapter.compute(raw, joints(q), joints(dq));
  std::copy(tau.begin(), tau.end(), output);
}
int sit_observation(void * handle, const double * values, float * output)
{
  tita::RobotState state;
  state.joint_pos = joints(values);
  state.joint_vel = joints(values+8);
  std::copy(values+16, values+20, state.quat_wxyz.begin());
  std::copy(values+20, values+23, state.ang_vel.begin());
  std::array<double, 3> command{};
  std::copy(values+23, values+26, command.begin());
  const std::vector<float> last(values+26, values+34);
  const auto result = static_cast<Bridge *>(handle)->observer.build(state, command, last);
  std::copy(result.begin(), result.end(), output);
  return static_cast<int>(result.size());
}
}
