#ifndef TITA_STAGE1_CONTROLLER__RL_PIPELINE_HPP_
#define TITA_STAGE1_CONTROLLER__RL_PIPELINE_HPP_

#include <array>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>

namespace tita_stage1_controller
{

constexpr std::size_t kRlJointCount = 8;
constexpr std::size_t kObservationSize = 33;
constexpr std::size_t kEstimatorSize = 3;

using FloatJointArray = std::array<float, kRlJointCount>;
using ObservationArray = std::array<float, kObservationSize>;
using EstimatorArray = std::array<float, kEstimatorSize>;

// Policy-order previous-action feedback for a bounded stand-to-RL blend.
// Alpha represents the RL contribution actually selected by the command path.
FloatJointArray applied_policy_action_feedback(
  const FloatJointArray & action_policy_order, float alpha);

struct ObservationInput
{
  FloatJointArray joint_position_native{};
  FloatJointArray joint_velocity_native{};
  std::array<float, 4> quaternion_xyzw{0.0F, 0.0F, 0.0F, 1.0F};
  std::array<float, 3> angular_velocity{};
  std::array<float, 3> command_vx_vy_yaw{};
  // Training ActionsCfg / ONNX output order: [L1, L2, L3, L4, R1, R2, R3, R4].
  // This is intentionally not the interleaved order used by joint observation fields.
  FloatJointArray previous_action_policy_order{};
};

struct ObservationResult
{
  ObservationArray values{};
  std::array<float, 3> projected_gravity{};
  bool finite{false};
};

class ObservationBuilder
{
public:
  ObservationResult build(const ObservationInput & input) const;
};

struct ActionTargets
{
  FloatJointArray action_policy_order{};
  FloatJointArray action_native_order{};
  FloatJointArray action_scaled_native{};
  // Exact policy semantics before safety limiting: legs are q, wheels are dq.
  FloatJointArray rl_target_native{};
  // Safety-limited command candidate. Any difference is explicit in clipping_mask.
  FloatJointArray limited_target_native{};
  std::array<bool, kRlJointCount> clipping_mask{};
  bool finite{false};
  unsigned int clipping_count{0};
};

class ActionAdapter
{
public:
  // Exact native MuJoCo/training semantics: no action or wheel-target clipping.
  // Leg operational envelopes are applied separately by the hardware controller.
  ActionTargets compute_native_policy(
    const FloatJointArray & action_policy_order) const;

  ActionTargets compute(
    const FloatJointArray & action_policy_order,
    float max_leg_delta_rad = 0.25F,
    float max_wheel_velocity_rad_s = 5.0F) const;

  ActionTargets apply_operational_envelope(
    ActionTargets targets, const FloatJointArray & lower_limits,
    const FloatJointArray & upper_limits) const;
};

struct PolicyStatus
{
  bool loaded{false};
  std::string detail;
  std::string policy_sha256;
  std::array<std::string, 2> input_names{};
  std::string output_name;
  std::string estimator_output_name;
  bool estimator_output_available{false};
};

class OnnxPolicyRunner
{
public:
  OnnxPolicyRunner();
  ~OnnxPolicyRunner();
  OnnxPolicyRunner(const OnnxPolicyRunner &) = delete;
  OnnxPolicyRunner & operator=(const OnnxPolicyRunner &) = delete;

  PolicyStatus load(
    const std::string & policy_path, const std::string & expected_sha256,
    bool require_estimator_output = false);
  bool infer(
    const ObservationArray & observation, FloatJointArray & action,
    double & inference_ms, std::string & error);
  bool infer(
    const ObservationArray & observation, FloatJointArray & action,
    EstimatorArray & estimator_scaled, double & inference_ms, std::string & error);
  const PolicyStatus & status() const {return status_;}

private:
  class Impl;
  std::unique_ptr<Impl> impl_;
  PolicyStatus status_;
};

}  // namespace tita_stage1_controller
#endif
