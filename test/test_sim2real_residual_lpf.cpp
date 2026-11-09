// DESKTOP_DRY_RUN / ROBOT_COMMAND_FREE_RUNTIME: no SDK, CAN or robot node.
#include <cassert>
#include <chrono>
#include <iostream>
#include <limits>
#include "tita_controller/residual_torque_filter.hpp"
#include "tita_controller/async_policy.hpp"
#include "tita_controller/stop_residual.hpp"
using namespace tita;

int main(int argc, char ** argv)
{
  assert(argc == 2);
  ResidualTorqueFilter filter, bypass;
  filter.configure(60.);
  const double alpha = -std::expm1(-2*std::acos(-1.)*60*.002);
  Joints expected{}, requested{};
  for (int tick = 0; tick < 100; ++tick) {
    if (tick%2 == 0) for (int j = 0; j < 8; ++j) requested[j] = std::sin(.13*tick+j)*8.;
    const auto actual = filter.update(requested,true);
    for (int j = 0; j < 8; ++j) {
      expected[j] += alpha*(requested[j]-expected[j]);
      assert(std::abs(actual[j]-expected[j]) < 1e-12);
    }
    assert(bypass.update(requested,true) == requested);
  }
  assert(filter.update(requested,false) == Joints{});
  expected.fill(0.);
  auto first = filter.update(requested,true);
  for (int j = 0; j < 8; ++j) assert(std::abs(first[j]-alpha*requested[j]) < 1e-12);
  for (double hz : std::array<double,3>{-1.,250.,std::numeric_limits<double>::quiet_NaN()}) {
    bool rejected=false;
    try {filter.configure(hz);} catch (const std::exception &) {rejected=true;}
    assert(rejected);
  }
  filter.configure(60.);
  PolicyMotorBridge bridge;
  PolicyOutput output;
  output.source.epoch=1; output.source.stop_epoch=1; output.source.rl=true;
  output.source.stop_allowed=true; output.source.sensed_ns=100000000;
  output.teacher_source_ns=100000000; output.sequence=1; output.residual.fill(4.);
  bridge.begin(1,100000000); bridge.accept(output);
  auto valid=bridge.decide(102000000,1,true,true,false);
  assert(valid.residual_valid && filter.update(valid.residual,valid.residual_valid)[0] > 0.);
  auto expired=bridge.decide(114000000,1,true,true,false);
  assert(expired.valid && !expired.residual_valid);
  assert(filter.update(expired.residual,expired.residual_valid) == Joints{});
  assert(!bridge.decide(102000000,2,true,true,false).residual_valid);

  Ort::Env env(ORT_LOGGING_LEVEL_WARNING,"lpf_shared_sensor_check");
  StopResidual residual(env,argv[1],false,{},true);
  RobotState state;
  state.joint_pos={0.,.8,-1.5,.1,0.,.8,-1.5,.2};
  state.pose_command={.1,-.08,.35};
  std::vector<float> observation(38,0.f), action(8,.12f);
  observation[0]=.1f; observation[1]=-.2f; observation[2]=.3f;
  observation[3]=.04f; observation[4]=-.02f; observation[5]=-.99f;
  for (int j=0;j<8;++j) {observation[9+j]=.01f*(j+1); observation[17+j]=.02f*(j+1);}
  observation[34]=.06f;
  Joints previous; previous.fill(2.);
  residual.allow(true); residual.set_applied_torque(previous); residual.step(state,observation,action);
  const auto history=residual.history();
  for (int j=0;j<6;++j) assert(history[396+j] == observation[j]);
  int n=402;
  for (int j : {0,2,4,1,3,5}) assert(history[n++] == observation[9+j]*2.f);
  for (int j : {0,2,4,6,1,3,5,7}) assert(history[n++] == observation[17+j]);
  for (int j=0;j<8;++j) assert(std::abs(history[396+28+j]-.2f)<1e-7);
  assert(history[438] == 0.f && history[439] == observation[34]);
  state.joint_pos[3]+=.1;
  observation[11]+=.02f; observation[13]+=.03f;
  residual.set_applied_torque(previous); residual.step(state,observation,action);
  assert(std::abs(residual.wheel_error()-.15*.5*.0925)<1e-8);
  residual.allow(false);
  assert(residual.torque() == Joints{});
  for (float x : residual.history()) assert(x == 0.f);

  // Pure ORT inference cost only; does not certify a 500Hz sensor/motor schedule.
  std::vector<double> durations;
  residual.allow(true);
  for (int i=0;i<1200;++i) {
    const auto start=std::chrono::steady_clock::now();
    residual.set_applied_torque(previous); residual.step(state,observation,action);
    const double us=std::chrono::duration<double,std::micro>(std::chrono::steady_clock::now()-start).count();
    if (i>=200) durations.push_back(us);
  }
  std::sort(durations.begin(),durations.end());
  std::cout << "PASS filter500Hz/held250Hz, bypass, gate/expiry/epoch reset, shared440-frame mapping, pre-filter history, measured wheel odometry\n";
  std::cout << "Residual-only ORT inference us: p50=" << durations[500] << " p99=" << durations[990] << " max=" << durations.back() << "\n";
}
