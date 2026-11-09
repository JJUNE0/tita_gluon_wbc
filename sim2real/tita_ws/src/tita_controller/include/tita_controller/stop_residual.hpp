// DESKTOP_DRY_RUN validated optional stationary residual. No hardware access here.
#pragma once

#include <memory>
#include <string>
#include <onnxruntime_cxx_api.h>
#include "tita_controller/adapter.hpp"
#include "tita_controller/residual_pose_gate.hpp"

namespace tita
{
class StopResidual
{
public:
  StopResidual(Ort::Env & env, const std::string & path, bool action_mode = false,
    std::array<double, 2> velocity_thresholds = {}, bool teacher_shared_sensors = false)
  : action_mode_(action_mode), teacher_shared_sensors_(teacher_shared_sensors), velocity_thresholds_(velocity_thresholds)
  {
    if (velocity_thresholds_ != (std::array<double, 2>{}) &&
      (!action_mode_ || !std::all_of(velocity_thresholds_.begin(), velocity_thresholds_.end(),
        [](double v) {return std::isfinite(v) && v > 0.;})))
      throw std::runtime_error("invalid residual velocity latch thresholds");
    Ort::SessionOptions options;
    options.SetIntraOpNumThreads(1);
    options.SetInterOpNumThreads(1);
    session_ = std::make_unique<Ort::Session>(env, path.c_str(), options);
    if (session_->GetInputCount() != 1 || session_->GetOutputCount() != 1) {
      throw std::runtime_error("residual requires one input/output");
    }
    const auto input_type = session_->GetInputTypeInfo(0);
    const auto output_type = session_->GetOutputTypeInfo(0);
    const auto input = input_type.GetTensorTypeAndShapeInfo();
    const auto output = output_type.GetTensorTypeAndShapeInfo();
    if (input.GetShape() != std::vector<int64_t>{1, 440} || output.GetShape() != std::vector<int64_t>{1, 8} ||
      input.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT ||
      output.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT)
    {
      throw std::runtime_error("residual requires float32 [1,440] -> [1,8]");
    }
    Ort::AllocatorWithDefaultOptions allocator;
    input_name_ = session_->GetInputNameAllocated(0, allocator).get();
    output_name_ = session_->GetOutputNameAllocated(0, allocator).get();
  }

  void reset()
  {
    enabled_ = initialized_ = history_ready_ = stationary_ = false;
    wheel_error_ = 0.;
    torque_.fill(0.);
    history_.fill(0.f);
  }

  void allow(bool allowed)
  {
    if (!allowed || !enabled_) reset();
    enabled_ = allowed;
  }

  // Selected REQUESTED torque, before the motor-loop LPF. This keeps the actor's
  // previous-residual channel in the same pre-filter units as training.
  void set_applied_torque(const Joints & torque)
  {
    for (double value : torque) {
      if (!std::isfinite(value) || std::abs(value) > (action_mode_ ? 1.00001 : 10.00001)) {
        throw std::runtime_error("invalid applied residual feedback");
      }
    }
    if (enabled_) torque_ = torque;
  }

  // Missing frames invalidate temporal history, not the fixed stop reference.
  void clear_history() {history_ready_ = false; history_.fill(0.f);}

  // Called at the saved actor period (4 ms torque / 20 ms action).
  // Previous residual is the selected Nm or normalized reference correction.
  void step(const RobotState & state, const std::vector<float> & teacher_observation,
    const std::vector<float> & teacher_action)
  {
    if (!enabled_) return;
    if (teacher_observation.size() != 38 || teacher_action.size() != 8) {
      throw std::runtime_error("residual requires matched pose Teacher38 / native action8");
    }
    const bool gated = velocity_thresholds_[0] > 0.;
    if (gated && (!std::isfinite(state.lin_vel_b[0]) || !std::isfinite(state.lin_vel_b[1]) ||
      !std::isfinite(state.ang_vel[2]))) throw std::runtime_error("non-finite residual latch velocity");
    const bool stationary = !gated ||
      (std::hypot(state.lin_vel_b[0], state.lin_vel_b[1]) < velocity_thresholds_[0] &&
      std::abs(state.ang_vel[2]) < velocity_thresholds_[1]);
    const bool shared_sensors = action_mode_ || teacher_shared_sensors_;
    constexpr Joints defaults{0., .8, -1.5, 0., 0., .8, -1.5, 0.};
    auto measured_q = state.joint_pos;
    if (teacher_shared_sensors_) {
      constexpr std::array<int, 6> legs{0, 1, 2, 4, 5, 6}, observed{0, 2, 4, 1, 3, 5};
      for (std::size_t i = 0; i < legs.size(); ++i)
        measured_q[legs[i]] = defaults[legs[i]] + teacher_observation[9+observed[i]];
      // Teacher's wheel angle is zeroed. The real encoder already contains its
      // measurement error; restore that measured signal without synthetic noise.
    }
    const auto & q = state.quat_wxyz;
    const double pitch = shared_sensors ? std::atan2(teacher_observation[3],
      std::hypot(teacher_observation[4], teacher_observation[5])) :
      std::asin(std::clamp(2.*(q[0]*q[2]-q[3]*q[1]), -1., 1.));
    std::array<double, 2> angles{};
    for (std::size_t side = 0; side < 2; ++side) {
      const auto j = side * 4;
      angles[side] = measured_q[j+3] + measured_q[j+1] + measured_q[j+2] + pitch;
      if (initialized_) {
        const double delta = angles[side] - previous_angles_[side];
        wheel_error_ += std::atan2(std::sin(delta), std::cos(delta)) * .5 * .0925;
      }
    }
    // Reacquire at the first stationary sample; preserve the actor history.
    if (gated && (!stationary || !stationary_)) wheel_error_ = 0.;
    stationary_ = stationary;
    previous_angles_ = angles;
    std::array<float, 44> frame{};
    std::size_t n = 0;
    if (shared_sensors) {
      for (std::size_t j = 0; j < 6; ++j) frame[n++] = teacher_observation[j];
    } else {
      for (double x : state.ang_vel) frame[n++] = x * .25;
      for (double x : projected_gravity(q)) frame[n++] = x;
    }
    if (shared_sensors) {
      for (int j : {0, 2, 4, 1, 3, 5}) frame[n++] = teacher_observation[9+j] * 2.f;
      for (int j : {0, 2, 4, 6, 1, 3, 5, 7}) frame[n++] = teacher_observation[17+j];
    } else {
      for (int j : {0, 1, 2, 4, 5, 6}) frame[n++] = (state.joint_pos[j]-defaults[j]) * 2.;
      for (double x : state.joint_vel) frame[n++] = x * .05;
    }
    constexpr Joints gains{2.8, 2., 2.8, 6., 2.8, 2., 2.8, 6.};
    for (std::size_t j = 0; j < 8; ++j) frame[n++] = teacher_action[j] / gains[j];
    for (double x : torque_) frame[n++] = x / (action_mode_ ? 1. : 10.);
    n += 3;  // Active residual still requires exact-zero velocity commands.
    // Match native float32 command encoding, including held nonnominal height.
    constexpr std::array<float, 3> nominal{0.f, 0.f, .335f}, scales{.5f, .3f, .1f};
    for (std::size_t j = 0; j < 3; ++j) {
      frame[n++] = (static_cast<float>(state.pose_command[j])-nominal[j])/scales[j];
    }
    for (std::size_t j = 0; j < n; ++j) {
      if (!std::isfinite(frame[j])) throw std::runtime_error("non-finite residual observation");
      frame[j] = std::clamp(frame[j], -10.f, 10.f);
    }
    frame[n++] = wheel_error_ * 5.;  // Saved optional velocity latch; no input clip.
    frame[n++] = teacher_observation[34];
    if (!std::isfinite(frame[42]) || !std::isfinite(frame[43])) {
      throw std::runtime_error("non-finite residual wheel/heading error");
    }
    if (!history_ready_) {
      for (std::size_t row = 0; row < 10; ++row) {
        std::copy(frame.begin(), frame.end(), history_.begin() + row * 44);
      }
    } else {
      for (std::size_t j = 0; j < 396; ++j) history_[j] = history_[j+44];
      std::copy(frame.begin(), frame.end(), history_.begin() + 396);
    }
    initialized_ = true;
    history_ready_ = true;
    const std::array<int64_t, 2> shape{1, 440};
    auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    auto tensor = Ort::Value::CreateTensor<float>(memory, history_.data(), history_.size(), shape.data(), shape.size());
    const char * inputs[] = {input_name_.c_str()};
    const char * outputs[] = {output_name_.c_str()};
    auto result = session_->Run(Ort::RunOptions{nullptr}, inputs, &tensor, 1, outputs, 1);
    const float * values = result[0].GetTensorData<float>();
    for (std::size_t j = 0; j < 8; ++j) {
      const double limit = action_mode_ ? 1. : 10.;
      if (!std::isfinite(values[j]) || std::abs(values[j]) > limit+0.00001) {
        throw std::runtime_error("invalid residual output");
      }
      torque_[j] = std::clamp<double>(values[j], -limit, limit);
    }
  }

  // Nm in legacy torque mode; normalized [-1,1] in reference-action mode.
  const Joints & torque() const {return torque_;}
  const std::array<float, 440> & history() const {return history_;}
  bool position_latched() const {return enabled_ && stationary_;}
  double wheel_error() const {return wheel_error_;}

private:
  std::unique_ptr<Ort::Session> session_;
  std::string input_name_, output_name_;
  bool action_mode_{false};
  bool teacher_shared_sensors_{false};
  std::array<double, 2> velocity_thresholds_{};
  bool stationary_{false};
  bool enabled_{false}, initialized_{false}, history_ready_{false};
  double wheel_error_{0.};
  std::array<double, 2> previous_angles_{};
  std::array<float, 440> history_{};
  Joints torque_{};
};
}  // namespace tita
