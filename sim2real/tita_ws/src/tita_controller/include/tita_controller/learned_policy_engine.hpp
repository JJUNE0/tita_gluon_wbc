// Worker-owned observation/history/ORT state. No hardware or ROS access.
#pragma once

#include <optional>
#include "tita_controller/async_policy.hpp"
#include "tita_controller/stop_residual.hpp"
#include "tita_controller/velocity_bias.hpp"

namespace tita
{
class LearnedPolicyEngine
{
public:
  LearnedPolicyEngine(Ort::Env & env, std::unique_ptr<Ort::Session> teacher,
    const std::string & residual_path, ObservationBuilder builder, WheelKinematics odometry, bool action_mode = false,
    std::array<double, 2> residual_velocity_thresholds = {}, bool teacher_shared_sensors = false)
  : teacher_(std::move(teacher)), residual_(env, residual_path, action_mode, residual_velocity_thresholds, teacher_shared_sensors), builder_(std::move(builder)),
    odometry_(std::move(odometry)), action_mode_(action_mode)
  {
    Ort::AllocatorWithDefaultOptions allocator;
    input_name_ = teacher_->GetInputNameAllocated(0, allocator).get();
    output_name_ = teacher_->GetOutputNameAllocated(0, allocator).get();
  }

  PolicyOutput step(const PolicyInput & input)
  {
    PolicyOutput output;
    output.source = input;
    output.started_ns = policy_now_ns();
    if (!initialized_ || input.epoch != epoch_) {
      builder_.reset(); residual_.reset(); action_.fill(0.f);
      previous_source_ns_ = teacher_source_ns_ = teacher_source_tick_ = next_teacher_ns_ = 0;
      epoch_ = input.epoch;
      stop_epoch_ = input.stop_epoch;
      initialized_ = true;
    }
    if (!input.rl) {
      builder_.reset(); residual_.reset(); action_.fill(0.f);
      previous_source_ns_ = teacher_source_ns_ = next_teacher_ns_ = 0;
      output.completed_ns = policy_now_ns();
      return output;
    }
    if (!input.sensed_ns || output.started_ns < input.sensed_ns) throw std::runtime_error("invalid worker sensor timestamp");
    if (input.stop_epoch != stop_epoch_)
    {
      residual_.reset();
      stop_epoch_ = input.stop_epoch;
    }
    if (previous_source_ns_ && input.sensed_ns > previous_source_ns_ &&
      input.sensed_ns-previous_source_ns_ > (action_mode_ ? PolicyMotorBridge::kTeacherMaxAgeNs :
        PolicyMotorBridge::kResidualMaxAgeNs)) residual_.clear_history();
    if (previous_source_ns_ && input.sensed_ns <= previous_source_ns_) throw std::runtime_error("nonmonotonic worker snapshot");
    const auto begin_observation = policy_now_ns();
    auto state = input.state;
    state.lin_vel_b = odometry_.linear_velocity(state);
    builder_.set_gyro_bias(input.gyro_bias);
    const double dt = previous_source_ns_ ? std::clamp((input.sensed_ns-previous_source_ns_)*1e-9,
      action_mode_ ? .005 : .001, action_mode_ ? .05 : .01) : (action_mode_ ? .02 : .004);
    previous_source_ns_ = input.sensed_ns;
    std::vector<float> applied(input.applied_action.begin(), input.applied_action.end());
    auto obs = builder_.build(state, input.command, applied, dt);
    if (obs.size() != output.observation.size()) throw std::runtime_error("async policy requires Teacher38");
    std::copy(obs.begin(), obs.end(), output.observation.begin());
    output.observation_us = (policy_now_ns()-begin_observation)*1e-3;
    if (action_mode_ || !next_teacher_ns_ || input.sensed_ns >= next_teacher_ns_) {
      const auto begin_teacher = policy_now_ns();
      action_ = infer(obs);
      output.teacher_us = (policy_now_ns()-begin_teacher)*1e-3;
      output.teacher_updated = true;
      teacher_source_ns_ = input.sensed_ns;
      teacher_source_tick_ = input.control_tick;
      next_teacher_ns_ = next_teacher_ns_ ? next_teacher_ns_ + 20000000 : input.sensed_ns + 20000000;
      if (next_teacher_ns_ <= input.sensed_ns) next_teacher_ns_ = input.sensed_ns + 20000000;
    }
    residual_.allow(input.stop_allowed);
    if (input.stop_allowed) {
      residual_.set_applied_torque(input.applied_residual);
      const auto begin_residual = policy_now_ns();
      residual_.step(state, obs, std::vector<float>(action_.begin(), action_.end()));
      output.residual_us = (policy_now_ns()-begin_residual)*1e-3;
      output.residual_updated = true;
    }
    output.latch_velocity_estimate = state.lin_vel_b;
    output.residual_position_latched = residual_.position_latched();
    output.residual_wheel_position_error_m = residual_.wheel_error();
    output.action = action_;
    output.residual = residual_.torque();
    output.teacher_source_ns = teacher_source_ns_;
    output.teacher_source_tick = teacher_source_tick_;
    output.completed_ns = policy_now_ns();
    return output;
  }

private:
  std::array<float, 8> infer(std::vector<float> & obs)
  {
    auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    const std::array<int64_t, 2> shape{1, 38};
    auto input = Ort::Value::CreateTensor<float>(memory, obs.data(), obs.size(), shape.data(), 2);
    const char * names[] = {input_name_.c_str()};
    const char * outputs[] = {output_name_.c_str()};
    auto result = teacher_->Run(Ort::RunOptions{nullptr}, names, &input, 1, outputs, 1);
    const float * values = result[0].GetTensorData<float>();
    std::array<float, 8> action;
    for (std::size_t i = 0; i < 8; ++i) {
      if (!std::isfinite(values[i])) throw std::runtime_error("non-finite async Teacher action");
      action[i] = values[i];
    }
    return action;
  }
  std::unique_ptr<Ort::Session> teacher_;
  StopResidual residual_;
  ObservationBuilder builder_;
  WheelKinematics odometry_;
  std::string input_name_, output_name_;
  std::array<float, 8> action_{};
  uint64_t epoch_{0}, stop_epoch_{0}, previous_source_ns_{0};
  uint64_t teacher_source_ns_{0}, teacher_source_tick_{0}, next_teacher_ns_{0};
  bool initialized_{false};
  bool action_mode_{false};
};
}  // namespace tita
