#include "tita_stage1_controller/rl_pipeline.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <vector>

#include <openssl/evp.h>
#include <onnxruntime_cxx_api.h>

namespace tita_stage1_controller
{
namespace
{
constexpr std::array<std::size_t, kRlJointCount> kPolicyReindex = {0, 4, 1, 5, 2, 6, 3, 7};
constexpr FloatJointArray kDefaultJointAnglesNative =
  {0.1F, 0.8F, -1.5F, 0.0F, 0.1F, 0.8F, -1.5F, 0.0F};
constexpr std::array<bool, kRlJointCount> kIsWheel =
  {false, false, false, true, false, false, false, true};

bool finite(const float value) {return std::isfinite(value);}

std::string sha256_file(const std::string & path)
{
  std::ifstream input(path, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open policy for SHA256: " + path);
  EVP_MD_CTX * context = EVP_MD_CTX_new();
  if (context == nullptr) throw std::runtime_error("EVP_MD_CTX_new failed");
  unsigned char digest[EVP_MAX_MD_SIZE]{};
  unsigned int digest_size = 0;
  try {
    if (EVP_DigestInit_ex(context, EVP_sha256(), nullptr) != 1) {
      throw std::runtime_error("EVP_DigestInit_ex failed");
    }
    std::array<char, 65536> buffer{};
    while (input) {
      input.read(buffer.data(), static_cast<std::streamsize>(buffer.size()));
      const auto count = input.gcount();
      if (count > 0 && EVP_DigestUpdate(context, buffer.data(), static_cast<std::size_t>(count)) != 1) {
        throw std::runtime_error("EVP_DigestUpdate failed");
      }
    }
    if (EVP_DigestFinal_ex(context, digest, &digest_size) != 1) {
      throw std::runtime_error("EVP_DigestFinal_ex failed");
    }
  } catch (...) {
    EVP_MD_CTX_free(context);
    throw;
  }
  EVP_MD_CTX_free(context);
  std::ostringstream output;
  output << std::hex << std::setfill('0');
  for (unsigned int index = 0; index < digest_size; ++index) {
    output << std::setw(2) << static_cast<unsigned int>(digest[index]);
  }
  return output.str();
}
}  // namespace

FloatJointArray applied_policy_action_feedback(
  const FloatJointArray & action_policy_order, const float alpha)
{
  FloatJointArray result{};
  if (!finite(alpha)) {
    result.fill(std::numeric_limits<float>::quiet_NaN());
    return result;
  }
  const float bounded_alpha = std::clamp(alpha, 0.0F, 1.0F);
  for (std::size_t index = 0; index < result.size(); ++index) {
    result[index] = bounded_alpha * action_policy_order[index];
  }
  return result;
}

ObservationResult ObservationBuilder::build(const ObservationInput & input) const
{
  ObservationResult result;
  for (const float value : input.joint_position_native) if (!finite(value)) return result;
  for (const float value : input.joint_velocity_native) if (!finite(value)) return result;
  for (const float value : input.quaternion_xyzw) if (!finite(value)) return result;
  for (const float value : input.angular_velocity) if (!finite(value)) return result;
  for (const float value : input.command_vx_vy_yaw) if (!finite(value)) return result;
  for (const float value : input.previous_action_policy_order) if (!finite(value)) return result;

  const float x = input.quaternion_xyzw[0];
  const float y = input.quaternion_xyzw[1];
  const float z = input.quaternion_xyzw[2];
  const float w = input.quaternion_xyzw[3];
  const float norm = std::sqrt(x * x + y * y + z * z + w * w);
  if (!finite(norm) || norm < 1.0e-6F) return result;
  const float qx = x / norm;
  const float qy = y / norm;
  const float qz = z / norm;
  const float qw = w / norm;
  // R(q)^T * [0, 0, -1], identical to real_obs_builder.py.
  result.projected_gravity = {
    -2.0F * (qx * qz - qy * qw),
    -2.0F * (qy * qz + qx * qw),
    -(1.0F - 2.0F * (qx * qx + qy * qy))};

  std::size_t offset = 0;
  for (const float value : input.angular_velocity) result.values[offset++] = value * 0.25F;
  for (const float value : result.projected_gravity) result.values[offset++] = value;
  result.values[offset++] = input.command_vx_vy_yaw[0] * 2.0F;
  result.values[offset++] = input.command_vx_vy_yaw[1] * 2.0F;
  result.values[offset++] = input.command_vx_vy_yaw[2] * 0.25F;

  FloatJointArray position = input.joint_position_native;
  position[3] = 0.0F;
  position[7] = 0.0F;
  for (const auto native_index : kPolicyReindex) {
    result.values[offset++] = position[native_index] - kDefaultJointAnglesNative[native_index];
  }
  for (const auto native_index : kPolicyReindex) {
    result.values[offset++] = input.joint_velocity_native[native_index] * 0.05F;
  }
  for (const float value : input.previous_action_policy_order) result.values[offset++] = value;
  if (offset != kObservationSize) return result;
  result.finite = std::all_of(result.values.begin(), result.values.end(), finite);
  return result;
}

ActionTargets ActionAdapter::compute(
  const FloatJointArray & action_policy_order, const float max_leg_delta_rad,
  const float max_wheel_velocity_rad_s) const
{
  ActionTargets result;
  result.action_policy_order = action_policy_order;
  if (!(finite(max_leg_delta_rad) && max_leg_delta_rad > 0.0F &&
    finite(max_wheel_velocity_rad_s) && max_wheel_velocity_rad_s > 0.0F)) return result;
  if (!std::all_of(action_policy_order.begin(), action_policy_order.end(), finite)) return result;

  // The custom policy action head is already native left-then-right order.
  // kPolicyReindex applies only to observation joint fields.
  result.action_native_order = action_policy_order;
  for (std::size_t index = 0; index < kRlJointCount; ++index) {
    const float scale = kIsWheel[index] ? 5.0F : 0.25F;
    const float scaled = result.action_native_order[index] * scale;
    result.action_scaled_native[index] = scaled;
    if (kIsWheel[index]) {
      result.rl_target_native[index] = scaled;
      const float limited = std::clamp(scaled, -max_wheel_velocity_rad_s, max_wheel_velocity_rad_s);
      result.limited_target_native[index] = limited;
      result.clipping_mask[index] = limited != scaled;
    } else {
      result.rl_target_native[index] = kDefaultJointAnglesNative[index] + scaled;
      const float limited = std::clamp(scaled, -max_leg_delta_rad, max_leg_delta_rad);
      result.limited_target_native[index] = kDefaultJointAnglesNative[index] + limited;
      result.clipping_mask[index] = limited != scaled;
    }
    result.clipping_count += result.clipping_mask[index] ? 1U : 0U;
  }
  result.finite = std::all_of(
    result.rl_target_native.begin(), result.rl_target_native.end(), finite) &&
    std::all_of(
    result.limited_target_native.begin(), result.limited_target_native.end(), finite);
  return result;
}

ActionTargets ActionAdapter::compute_native_policy(
  const FloatJointArray & action_policy_order) const
{
  ActionTargets result;
  result.action_policy_order = action_policy_order;
  if (!std::all_of(action_policy_order.begin(), action_policy_order.end(), finite)) return result;
  result.action_native_order = action_policy_order;
  for (std::size_t index = 0; index < kRlJointCount; ++index) {
    const float scale = kIsWheel[index] ? 5.0F : 0.25F;
    const float scaled = result.action_native_order[index] * scale;
    result.action_scaled_native[index] = scaled;
    result.rl_target_native[index] = kIsWheel[index] ?
      scaled : kDefaultJointAnglesNative[index] + scaled;
    result.limited_target_native[index] = result.rl_target_native[index];
  }
  result.finite = std::all_of(
    result.rl_target_native.begin(), result.rl_target_native.end(), finite);
  return result;
}

ActionTargets ActionAdapter::apply_operational_envelope(
  ActionTargets targets, const FloatJointArray & lower_limits,
  const FloatJointArray & upper_limits) const
{
  if (!targets.finite ||
    !std::all_of(lower_limits.begin(), lower_limits.end(), finite) ||
    !std::all_of(upper_limits.begin(), upper_limits.end(), finite))
  {
    targets.finite = false;
    return targets;
  }

  for (std::size_t index = 0; index < kRlJointCount; ++index) {
    if (kIsWheel[index]) continue;
    if (lower_limits[index] > upper_limits[index]) {
      targets.finite = false;
      return targets;
    }
    const float previous = targets.limited_target_native[index];
    const float limited = std::clamp(previous, lower_limits[index], upper_limits[index]);
    targets.limited_target_native[index] = limited;
    if (limited != previous && !targets.clipping_mask[index]) {
      targets.clipping_mask[index] = true;
      ++targets.clipping_count;
    }
  }
  targets.finite = std::all_of(
    targets.limited_target_native.begin(), targets.limited_target_native.end(), finite);
  return targets;
}

class OnnxPolicyRunner::Impl
{
public:
  Ort::Env environment{ORT_LOGGING_LEVEL_WARNING, "tita_stage2_policy"};
  Ort::SessionOptions options;
  std::unique_ptr<Ort::Session> session;
  Ort::MemoryInfo memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  ObservationArray observation{};
  FloatJointArray action{};
  EstimatorArray estimator{};
  std::array<int64_t, 2> observation_shape{1, static_cast<int64_t>(kObservationSize)};
  std::array<int64_t, 2> action_shape{1, static_cast<int64_t>(kRlJointCount)};
  std::array<int64_t, 2> estimator_shape{1, static_cast<int64_t>(kEstimatorSize)};
  std::array<std::string, 2> input_name_storage{};
  std::string output_name_storage;
  std::string estimator_output_name_storage;
  std::array<const char *, 1> input_names{};
  std::array<const char *, 2> output_names{};
  std::vector<Ort::Value> input_values;
  std::vector<Ort::Value> output_values;

  Impl()
  {
    options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);
    options.SetIntraOpNumThreads(1);
    options.SetInterOpNumThreads(1);
    options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    input_values.reserve(1);
    input_values.emplace_back(Ort::Value::CreateTensor<float>(
      memory, observation.data(), observation.size(),
      observation_shape.data(), observation_shape.size()));
    output_values.reserve(2);
    output_values.emplace_back(Ort::Value::CreateTensor<float>(
      memory, action.data(), action.size(), action_shape.data(), action_shape.size()));
    output_values.emplace_back(Ort::Value::CreateTensor<float>(
      memory, estimator.data(), estimator.size(),
      estimator_shape.data(), estimator_shape.size()));
  }
};

OnnxPolicyRunner::OnnxPolicyRunner() : impl_(std::make_unique<Impl>()) {}
OnnxPolicyRunner::~OnnxPolicyRunner() = default;

PolicyStatus OnnxPolicyRunner::load(
  const std::string & policy_path, const std::string & expected_sha256,
  const bool require_estimator_output)
{
  status_ = PolicyStatus{};
  try {
    status_.policy_sha256 = sha256_file(policy_path);
    if (!expected_sha256.empty() && status_.policy_sha256 != expected_sha256) {
      throw std::runtime_error("policy SHA256 mismatch");
    }
    impl_->session = std::make_unique<Ort::Session>(
      impl_->environment, policy_path.c_str(), impl_->options);
    const auto output_count = impl_->session->GetOutputCount();
    if (impl_->session->GetInputCount() != 1U || output_count < 1U || output_count > 2U) {
      throw std::runtime_error("policy must expose one input and one or two outputs");
    }
    Ort::AllocatorWithDefaultOptions allocator;
    bool observation_found = false;
    for (std::size_t index = 0; index < 1U; ++index) {
      const auto shape = impl_->session->GetInputTypeInfo(index).GetTensorTypeAndShapeInfo().GetShape();
      auto name = impl_->session->GetInputNameAllocated(index, allocator);
      if (shape == std::vector<int64_t>({1, static_cast<int64_t>(kObservationSize)})) {
        impl_->input_name_storage[0] = name.get();
        observation_found = true;
      } else {
        throw std::runtime_error("unexpected policy input shape");
      }
    }
    bool action_found = false;
    bool estimator_found = false;
    for (std::size_t index = 0; index < output_count; ++index) {
      const auto shape =
        impl_->session->GetOutputTypeInfo(index).GetTensorTypeAndShapeInfo().GetShape();
      auto name = impl_->session->GetOutputNameAllocated(index, allocator);
      if (shape == std::vector<int64_t>({1, static_cast<int64_t>(kRlJointCount)})) {
        if (action_found) throw std::runtime_error("duplicate action output");
        impl_->output_name_storage = name.get();
        action_found = true;
      } else if (shape == std::vector<int64_t>({1, static_cast<int64_t>(kEstimatorSize)})) {
        if (estimator_found) throw std::runtime_error("duplicate estimator output");
        impl_->estimator_output_name_storage = name.get();
        estimator_found = true;
      } else {
        throw std::runtime_error("unexpected policy output shape");
      }
    }
    if (!observation_found) throw std::runtime_error("required policy input missing");
    if (!action_found) throw std::runtime_error("required action output missing");
    if (require_estimator_output && !estimator_found) {
      throw std::runtime_error("required estimator output missing");
    }
    impl_->input_names = {impl_->input_name_storage[0].c_str()};
    impl_->output_names[0] = impl_->output_name_storage.c_str();
    impl_->output_names[1] = estimator_found ?
      impl_->estimator_output_name_storage.c_str() : nullptr;
    status_.input_names = impl_->input_name_storage;
    status_.output_name = impl_->output_name_storage;
    status_.estimator_output_name = impl_->estimator_output_name_storage;
    status_.estimator_output_available = estimator_found;
    status_.loaded = true;
    status_.detail = estimator_found ?
      "loaded and validated fixed [1,33] -> [1,8] action + [1,3] estimator interface" :
      "loaded and validated fixed [1,33]/[1,8] interface";
  } catch (const std::exception & error) {
    impl_->session.reset();
    status_.loaded = false;
    status_.detail = error.what();
  }
  return status_;
}

bool OnnxPolicyRunner::infer(
  const ObservationArray & observation, FloatJointArray & action,
  double & inference_ms, std::string & error)
{
  EstimatorArray ignored{};
  return infer(observation, action, ignored, inference_ms, error);
}

bool OnnxPolicyRunner::infer(
  const ObservationArray & observation, FloatJointArray & action,
  EstimatorArray & estimator_scaled, double & inference_ms, std::string & error)
{
  if (!status_.loaded || !impl_->session) {
    error = status_.detail.empty() ? "policy is not loaded" : status_.detail;
    return false;
  }
  if (!std::all_of(observation.begin(), observation.end(), finite)) {
    error = "non-finite ONNX input";
    return false;
  }
  impl_->observation = observation;
  impl_->action.fill(0.0F);
  impl_->estimator.fill(0.0F);
  try {
    const auto started = std::chrono::steady_clock::now();
    impl_->session->Run(
      Ort::RunOptions{nullptr}, impl_->input_names.data(), impl_->input_values.data(),
      impl_->input_values.size(), impl_->output_names.data(), impl_->output_values.data(),
      status_.estimator_output_available ? 2U : 1U);
    inference_ms = std::chrono::duration<double, std::milli>(
      std::chrono::steady_clock::now() - started).count();
  } catch (const std::exception & exception) {
    error = exception.what();
    return false;
  }
  if (!std::all_of(impl_->action.begin(), impl_->action.end(), finite)) {
    error = "non-finite ONNX output";
    return false;
  }
  if (status_.estimator_output_available &&
    !std::all_of(impl_->estimator.begin(), impl_->estimator.end(), finite))
  {
    error = "non-finite estimator output";
    return false;
  }
  action = impl_->action;
  estimator_scaled = impl_->estimator;
  error.clear();
  return true;
}

}  // namespace tita_stage1_controller
