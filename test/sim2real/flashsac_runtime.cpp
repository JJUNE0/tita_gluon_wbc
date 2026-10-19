// DESKTOP_DRY_RUN: exercise the real C++ state machine and ONNX Runtime without ROS/CAN.
#include <cmath>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <onnxruntime_cxx_api.h>
#include "tita_controller/state_machine.hpp"

void require(bool ok, const char * message)
{
  if (!ok) throw std::runtime_error(message);
}

void check_states()
{
  using namespace tita;
  StateMachine sm(Joints{60., 60., 60., 12., 60., 60., 60., 12.});
  const Joints velocity{1., -1., 2., -2., 1., -1., 2., -2.};
  const Joints expected_damping{-8., 8., -16., 1., -8., 8., -16., 1.};
  require(sm.state() == State::Idle, "startup must be idle");
  require(sm.torque(kSplayPose, velocity) == expected_damping, "idle must retain original damping");
  require(sm.torque(kSitPose, velocity) == expected_damping, "idle damping must not depend on pose");
  require(sm.torque(kSitPose, Joints{}) == Joints{}, "idle at rest must produce zero torque");
  const Joints fast_velocity{100., -100., 100., -100., 100., -100., 100., -100.};
  const Joints clipped_damping{-60., 60., -60., 12., -60., 60., -60., 12.};
  require(sm.torque(kSitPose, fast_velocity) == clipped_damping, "idle damping must obey torque limits");
  require(!sm.request(State::Rl, kSplayPose), "idle must reject direct RL");
  sm.request(State::TransformUp, kSplayPose);
  sm.update(.5);
  require(!sm.request(State::Rl, kSplayPose), "incomplete transform must reject RL");
  for (int tick = 0; tick < 1000; ++tick) sm.update(.002);
  require(sm.state() == State::Sit, "transform must finish in ready/sit");
  require(sm.request(State::Rl, kSitPose), "ready must allow RL");
  sm.request(State::Idle, kSitPose);
  require(sm.torque(kSitPose, velocity) == expected_damping, "return to idle must restore damping");
  sm.request(State::Damp, kSitPose);
  const auto damp = sm.torque(kSitPose, velocity);
  require(damp == expected_damping, "idle and fault damp must use the same original gains");
  for (std::size_t i = 0; i < 8; ++i) {
    require(damp[i] * velocity[i] < 0., "fault damping must oppose motion");
  }
  require(!sm.request(State::Rl, kSitPose), "fault recovery requires transform again");
}

int main(int argc, char ** argv)
{
  if (argc != 3) return 2;
  check_states();
  Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "flashsac_test");
  Ort::SessionOptions options;
  options.SetIntraOpNumThreads(1);
  Ort::Session policy(env, argv[1], options);
  Ort::AllocatorWithDefaultOptions allocator;
  const auto in = policy.GetInputNameAllocated(0, allocator);
  const auto out = policy.GetOutputNameAllocated(0, allocator);
  const char * input_names[] = {in.get()};
  const char * output_names[] = {out.get()};
  require(policy.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1] == 33,
    "expected 33 observations");
  require(policy.GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1] == 8,
    "expected eight actions");
  auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  const int64_t shape[] = {1, 33};
  std::ifstream fixture(argv[2]);
  require(bool(fixture), "missing observation fixture");
  std::vector<float> obs(33);
  std::cout.precision(10);
  while (fixture >> obs[0]) {
    for (int i = 1; i < 33; ++i) require(bool(fixture >> obs[i]), "incomplete fixture");
    auto tensor = Ort::Value::CreateTensor<float>(memory, obs.data(), obs.size(), shape, 2);
    auto first = policy.Run(Ort::RunOptions{nullptr}, input_names, &tensor, 1, output_names, 1);
    auto second = policy.Run(Ort::RunOptions{nullptr}, input_names, &tensor, 1, output_names, 1);
    const auto * a = first[0].GetTensorData<float>();
    const auto * b = second[0].GetTensorData<float>();
    for (int i = 0; i < 8; ++i) {
      require(std::isfinite(a[i]) && a[i] == b[i], "actor must be finite and deterministic");
      std::cout << a[i] << (i == 7 ? '\n' : ' ');
    }
  }
}
