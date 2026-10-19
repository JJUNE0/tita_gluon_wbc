// One control loop for policy, motors and joystick: same structure as sim2sim_node.py,
// with the MuJoCo env replaced by the TITA CAN API.
//
// Lower buttons: hold right >=1 s from idle -> transform_up; left down -> RL
// after sit; left up -> return_to_sit; a NEW right press -> latched supporting sit (faults use damping).
// Default left/right axes 4/6 follow the DDT two-position-channel convention;
// physical button mapping must be checked with motor output disabled.
// Sticks: axes[2] forward/back, axes[3] yaw.

#include <atomic>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <limits>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "std_msgs/msg/string.hpp"
#include "tita_controller/adapter.hpp"
#include "tita_controller/control_loop_exit.hpp"
#include "tita_controller/joystick_buttons.hpp"
#include "tita_controller/leg_action_filter.hpp"
#include "tita_controller/state_machine.hpp"
#include "tita_controller/msg/training_sample.hpp"
#include "tita_controller/msg/motor_feedback.hpp"
#include "tita_controller/msg/action_filter_sample.hpp"
#include "tita_controller/velocity_bias.hpp"
#include "tita_robot/tita_robot.hpp"

namespace tita
{
constexpr double kLoopDt = 0.002;     // 500 Hz motor loop
constexpr double kFallTilt = 0.65;    // rad; beyond this -> damp
constexpr double kJoyTimeout = 0.5;   // s; stale joystick after enabling -> latched stop
constexpr double kCommandRamp = 0.5;  // units/s, same as sim2sim keyboard
// Heading gyro bias: median of the latest stationary Idle/Sit gyro z samples, taken on RL entry.
constexpr std::size_t kGyroBiasWindow = 2500;     // 5 s at 500 Hz
constexpr std::size_t kGyroBiasMinSamples = 500;  // 1 s
constexpr double kStillJointVel = 0.02;           // rad/s, every joint
constexpr double kStillGyro = 0.05;               // rad/s, every axis

const std::vector<std::string> kJointNames{
  "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
  "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4"};

class TitaNode : public rclcpp::Node
{
public:
  TitaNode()
  : Node("tita"),
    sm_(joints("torque_limit")),
    obs_builder_(obs_layout(), joints("default_joint_angles"), joints("default_joint_velocities"), position_config(),
      heading_config()),
    action_adapter_(action_terms(), joints("joint_kp"), joints("joint_kd"), joints("torque_limit")),
    leg_filter_(declare_parameter("leg_action_filter", std::string("none")),
      param<std::vector<int64_t>>("action_joint"),
      declare_parameter("leg_notch_hz", 8.3), declare_parameter("leg_notch_q", 3.)),
    env_(ORT_LOGGING_LEVEL_WARNING, "tita"),
    robot_(8)
  {
    output_enabled_ = declare_parameter("output_enabled", false);
    left_button_axis_ = declare_parameter("left_button_axis", 4);
    right_button_axis_ = declare_parameter("right_button_axis", 6);
    if (left_button_axis_ < 4 || right_button_axis_ < 4 ||
      left_button_axis_ > 7 || right_button_axis_ > 7 || left_button_axis_ == right_button_axis_)
    {
      throw std::runtime_error("button axes must be distinct indices in [4, 7]");
    }
    heading_bias_fallback_ = declare_parameter("heading_gyro_bias_fallback", 0.);
    if (!std::isfinite(heading_bias_fallback_)) throw std::runtime_error("non-finite heading gyro bias fallback");
    if (obs_builder_.heading_enabled()) {
      gyro_samples_.reserve(kGyroBiasWindow);
      RCLCPP_INFO(get_logger(), "heading error observation ON: gyro z bias = median of the last %.0f s of "
        "stationary idle/sit samples on RL entry (min %.0f s, else fallback %.5f rad/s)",
        kGyroBiasWindow * kLoopDt, kGyroBiasMinSamples * kLoopDt, heading_bias_fallback_);
    }
    max_lin_x_ = declare_parameter("max_lin_x", 0.2);
    max_ang_z_ = declare_parameter("max_ang_z", 0.3);
    const double policy_dt = param<double>("policy_dt");
    if (!std::isfinite(policy_dt) || policy_dt < kLoopDt || policy_dt > 1. ||
      std::abs(policy_dt / kLoopDt - std::round(policy_dt / kLoopDt)) > 1e-6)
    {
      throw std::runtime_error("policy_dt must be a positive multiple of 0.002 s, at most 1 s");
    }
    decimation_ = static_cast<int>(std::lround(policy_dt / kLoopDt));
    if (leg_filter_.mode() != "none" && std::abs(policy_dt - .02) > 1e-9) {
      throw std::runtime_error("leg action MA2 requires a 20 ms policy period");
    }
    if (declare_parameter("velocity_bias", false)) {
      if (std::abs(policy_dt - .02) > 1e-9) {
        throw std::runtime_error("velocity bias requires a 20 ms policy period");
      }
      const double sign = declare_parameter("velocity_bias_response_sign", 1.);
      const auto kd = joints("joint_kd");
      velocity_bias_ = std::make_unique<WheelVelocityBias>(
        param<std::vector<double>>("velocity_bias_xyz"),
        param<std::vector<double>>("velocity_bias_rpy"),
        param<std::vector<double>>("velocity_bias_axis"),
        param<double>("velocity_bias_radius"), sign, std::array<double, 2>{kd[3], kd[7]});
      RCLCPP_WARN(get_logger(), "velocity bias ON: ignore 0-1 s, estimate 1-3 s, apply after 3 s; "
        "additional torque <=0.8 Nm/wheel; ramp 1 s, slew <=0.8 Nm/s; no torque seed; "
        "pitch deviation cutoff 5 deg; response_sign=%.0f "
        "(hardware feedback sign NOT_TESTED)", sign);
    }
    Ort::SessionOptions options;
    options.SetIntraOpNumThreads(1);
    policy_ = std::make_unique<Ort::Session>(env_, param<std::string>("policy_path").c_str(), options);
    if (policy_->GetInputCount() != 1 || policy_->GetOutputCount() != 1) {
      throw std::runtime_error("policy needs one observation input and one action output");
    }
    const auto input_shape = policy_->GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape();
    const auto output_shape = policy_->GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape();
    const auto obs_size = static_cast<int64_t>(param<std::vector<int64_t>>("obs_kind").size());
    if (input_shape.size() != 2 || (input_shape[0] != 1 && input_shape[0] != -1) ||
      input_shape[1] != obs_size || output_shape.size() != 2 ||
      (output_shape[0] != 1 && output_shape[0] != -1) || output_shape[1] != 8)
    {
      throw std::runtime_error("policy tensor shapes do not match configured observation / 8 actions");
    }
    last_action_.assign(8, 0.f);
    applied_action_.assign(8, 0.f);

    const auto ns = declare_parameter("namespace", std::string(""));
    joy_sub_ = create_subscription<sensor_msgs::msg::Joy>(
      declare_parameter("joy_topic", std::string("/joy")), 10, [this](sensor_msgs::msg::Joy::SharedPtr m) {
        std::lock_guard<std::mutex> lock(joy_mutex_);
        joy_ = *m;
        joy_time_ = std::chrono::steady_clock::now();
      });
    joint_pub_ = create_publisher<sensor_msgs::msg::JointState>(ns + "/joint_states", 10);
    imu_pub_ = create_publisher<sensor_msgs::msg::Imu>(ns + "/imu_sensor_broadcaster/imu", 10);
    obs_pub_ = create_publisher<std_msgs::msg::Float32MultiArray>("/sim2real/debug/obs", 10);
    action_pub_ = create_publisher<std_msgs::msg::Float32MultiArray>("/sim2real/debug/action", 10);
    torque_pub_ = create_publisher<std_msgs::msg::Float32MultiArray>("/sim2real/debug/torque", 10);
    bias_pub_ = create_publisher<std_msgs::msg::Float32MultiArray>("/sim2real/debug/velocity_bias", 10);
    state_pub_ = create_publisher<std_msgs::msg::String>("/sim2real/debug/state", 10);
    training_pub_ = create_publisher<tita_controller::msg::TrainingSample>("/sim2real/training_sample", 10);
    feedback_pub_ = create_publisher<tita_controller::msg::MotorFeedback>("/sim2real/motor_feedback", 10);
    filter_pub_ = create_publisher<tita_controller::msg::ActionFilterSample>("/sim2real/action_filter_sample", 10);
    RCLCPP_INFO(get_logger(), "leg action filter: %s; raw last_action, applied targets logged",
      leg_filter_.mode().c_str());
    if (leg_filter_.mode() == "ma2_notch_legs") {
      RCLCPP_INFO(get_logger(), "leg notch: %.3f Hz, Q %.3f at 50 Hz; hardware attenuation NOT_TESTED",
        param<double>("leg_notch_hz"), param<double>("leg_notch_q"));
    }
    RCLCPP_WARN(get_logger(), "motor output %s; state: idle; policy %.1f Hz",
      output_enabled_ ? "ENABLED" : "DISABLED", 1. / policy_dt);
    RCLCPP_INFO(get_logger(), "buttons: left axes[%d], right axes[%d]; release both first; "
      "hold right >=1 s to prepare, release/repress right to latch supporting sit until restart",
      left_button_axis_, right_button_axis_);
    loop_ = std::thread([this] {
      const auto exit = run_with_torque_release(
        [this] {run();}, output_enabled_,
        [this] {return robot_.set_target_joint_t(std::vector<double>(8, 0.));},
        [] {std::this_thread::sleep_for(std::chrono::milliseconds(2));});
      if (exit.loop_error) {
        try {std::rethrow_exception(exit.loop_error);}
        catch (const std::exception & e) {
          RCLCPP_ERROR(get_logger(), "control loop exited with exception: %s", e.what());
        } catch (...) {
          RCLCPP_ERROR(get_logger(), "control loop exited with unknown exception");
        }
      }
      if (exit.zero_requested) {
        if (exit.zero_failed) {
          RCLCPP_ERROR(get_logger(),
            "shutdown zero-torque transmission FAILED (%zu/%zu accepted); "
            "motor torque may remain. Physical power isolation is required.",
            exit.accepted, exit.attempts);
        } else {
          RCLCPP_WARN(get_logger(),
            "shutdown zero-torque commands sent (%zu); transport accepted, "
            "motor acknowledgement/power isolation not confirmed", exit.accepted);
        }
      }
    });
  }

  ~TitaNode() override
  {
    running_ = false;
    if (loop_.joinable()) loop_.join();
  }

private:
  // Required parameter (set by tita.launch.py); safe to read more than once.
  template<class T>
  T param(const std::string & name)
  {
    if (!has_parameter(name)) declare_parameter<T>(name);
    return get_parameter(name).get_value<T>();
  }

  Joints joints(const std::string & name)
  {
    const auto values = param<std::vector<double>>(name);
    if (values.size() != 8) throw std::runtime_error(name + " needs 8 values");
    Joints result{};
    std::copy(values.begin(), values.end(), result.begin());
    return result;
  }

  std::vector<ObsElement> obs_layout()
  {
    const auto kind = param<std::vector<int64_t>>("obs_kind");
    const auto index = param<std::vector<int64_t>>("obs_index");
    const auto scale = param<std::vector<double>>("obs_scale");
    const auto low = param<std::vector<double>>("obs_low");
    const auto high = param<std::vector<double>>("obs_high");
    std::vector<ObsElement> layout;
    for (std::size_t i = 0; i < kind.size(); ++i) {
      layout.push_back({static_cast<int>(kind[i]), static_cast<int>(index[i]), scale[i], low[i], high[i]});
    }
    return layout;
  }

  std::vector<ActionTerm> action_terms()
  {
    const auto joint = param<std::vector<int64_t>>("action_joint");
    const auto velocity = param<std::vector<bool>>("action_velocity");
    const auto scale = param<std::vector<double>>("action_scale");
    const auto offset = param<std::vector<double>>("action_offset");
    const auto low = param<std::vector<double>>("action_low");
    const auto high = param<std::vector<double>>("action_high");
    std::vector<ActionTerm> terms;
    for (std::size_t i = 0; i < joint.size(); ++i) {
      terms.push_back({static_cast<int>(joint[i]), velocity[i], scale[i], offset[i], low[i], high[i]});
    }
    return terms;
  }

  WheelPositionConfig position_config()
  {
    WheelPositionConfig cfg;
    cfg.radius = declare_parameter("wheel_position_radius", 0.);
    cfg.clip_m = declare_parameter("wheel_position_clip_m", 0.);
    const auto thresholds = declare_parameter("wheel_position_zero_thresholds", std::vector<double>{0., 0., 0.});
    if (thresholds.size() != 3) throw std::runtime_error("wheel position zero thresholds need 3 values");
    std::copy(thresholds.begin(), thresholds.end(), cfg.zero_thresholds.begin());
    return cfg;
  }

  HeadingConfig heading_config()
  {
    HeadingConfig cfg;
    cfg.clip_rad = declare_parameter("heading_clip_rad", 0.);
    cfg.warmup_s = declare_parameter("heading_warmup_s", 0.);
    cfg.dt = param<double>("policy_dt");
    const auto thresholds = declare_parameter("heading_zero_thresholds", std::vector<double>{0., 0., 0.});
    if (thresholds.size() != 3) throw std::runtime_error("heading zero thresholds need 3 values");
    std::copy(thresholds.begin(), thresholds.end(), cfg.zero_thresholds.begin());
    return cfg;
  }

  // Stationary gyro z samples while idle/sit; the newest kGyroBiasWindow are kept.
  void sample_gyro_bias(const RobotState & s, bool valid)
  {
    const auto state = sm_.state();
    if (!valid || (state != State::Idle && state != State::Sit)) return;
    for (double v : s.joint_vel) if (std::abs(v) >= kStillJointVel) return;
    for (double w : s.ang_vel) if (std::abs(w) >= kStillGyro) return;
    if (gyro_samples_.size() < kGyroBiasWindow) {
      gyro_samples_.push_back(s.ang_vel[2]);
    } else {
      gyro_samples_[gyro_next_] = s.ang_vel[2];
    }
    gyro_next_ = (gyro_next_ + 1) % kGyroBiasWindow;
  }

  void apply_gyro_bias()
  {
    double bias = heading_bias_fallback_;
    if (gyro_samples_.size() >= kGyroBiasMinSamples) {
      auto values = gyro_samples_;
      std::nth_element(values.begin(), values.begin() + values.size() / 2, values.end());
      bias = values[values.size() / 2];
      RCLCPP_INFO(get_logger(), "heading gyro bias %.5f rad/s (%.3f deg/s) from %zu stationary samples",
        bias, bias * 180. / M_PI, gyro_samples_.size());
    } else {
      RCLCPP_WARN(get_logger(), "heading gyro bias: only %zu stationary samples (< %zu); using fallback %.5f rad/s",
        gyro_samples_.size(), kGyroBiasMinSamples, bias);
    }
    obs_builder_.set_gyro_bias(bias);
  }

  // Returns false when IMU/motor data is stale or non-finite.
  bool read(RobotState & s)
  {
    if (robot_.imu_data_timeout() || robot_.motors_data_timeout()) return false;
    const auto q = robot_.get_joint_q(), v = robot_.get_joint_v();
    const auto quat = robot_.get_imu_quaternion();  // x y z w
    const auto gyro = robot_.get_imu_angular_velocity();
    if (q.size() != 8 || v.size() != 8) return false;
    for (std::size_t i = 0; i < 8; ++i) {
      s.joint_pos[i] = q[i];
      s.joint_vel[i] = v[i];
      if (i % 4 == 1 && s.joint_pos[i] < -2.5) s.joint_pos[i] += 2 * M_PI;  // leg_2 encoder wrap
    }
    s.quat_wxyz = {quat[3], quat[0], quat[1], quat[2]};
    s.ang_vel = {gyro[0], gyro[1], gyro[2]};
    bool finite = true;
    for (double x : s.joint_pos) finite &= std::isfinite(x);
    for (double x : s.joint_vel) finite &= std::isfinite(x);
    for (double x : s.quat_wxyz) finite &= std::isfinite(x);
    for (double x : s.ang_vel) finite &= std::isfinite(x);
    double norm_squared = 0.;
    for (double x : s.quat_wxyz) norm_squared += x * x;
    if (!finite || std::abs(norm_squared - 1.) > .1) return false;
    for (double & x : s.quat_wxyz) x /= std::sqrt(norm_squared);
    return true;
  }

  // Button edges are handled before faults so right press can latch even if sensors fail.
  void handle_joystick(const RobotState & s, bool sensors_valid, const Joints & previous_torque)
  {
    sensor_msgs::msg::Joy joy;
    bool fresh;
    {
      std::lock_guard<std::mutex> lock(joy_mutex_);
      joy = joy_;
      fresh = std::chrono::duration<double>(std::chrono::steady_clock::now() - joy_time_).count() < kJoyTimeout;
    }
    std::array<double, 3> target{};
    const bool finite = std::all_of(joy.axes.begin(), joy.axes.end(),
      [](float x) {return std::isfinite(x);});
    const bool enough_axes = joy.axes.size() > static_cast<std::size_t>(
      std::max(left_button_axis_, right_button_axis_));
    const auto left = enough_axes ? button_down(joy.axes[left_button_axis_]) : std::nullopt;
    const auto right = enough_axes ? button_down(joy.axes[right_button_axis_]) : std::nullopt;
    const bool valid = fresh && finite && left.has_value() && right.has_value();
    const auto event = buttons_.update(valid, left.value_or(false), right.value_or(false),
      std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count());
    if (event == ButtonEvent::Stop) {
      sm_.request(State::EStop, s.joint_pos, previous_torque);
      RCLCPP_ERROR(get_logger(), "software stop latched: new right press or joystick invalid/stale; "
        "upright: supporting sit over 4 s; sensor/fall fault: damping; restart required");
    } else if (sensors_valid) {
      if (event == ButtonEvent::TransformUp &&
        (sm_.state() == State::Idle || sm_.state() == State::Damp))
      {
        sm_.request(State::TransformUp, s.joint_pos);
      } else if (event == ButtonEvent::Rl && !sm_.request(State::Rl, s.joint_pos)) {
        RCLCPP_WARN(get_logger(), "rl rejected: wait for sit, then release/repress left button");
      } else if (event == ButtonEvent::ReturnToSit && sm_.state() == State::Rl) {
        sm_.request(State::ReturnToSit, s.joint_pos, previous_torque);
      }
    }
    if (valid && sensors_valid && sm_.state() == State::Rl) {
      target = {-std::clamp<double>(joy.axes[2], -1, 1) * max_lin_x_, 0.,
        std::clamp<double>(joy.axes[3], -1, 1) * max_ang_z_};
    }
    if (sm_.state() != State::Rl) {
      command_.fill(0.);
      return;
    }
    for (std::size_t i = 0; i < 3; ++i) {
      command_[i] += std::clamp(target[i] - command_[i], -kCommandRamp * kLoopDt, kCommandRamp * kLoopDt);
    }
  }

  void run()
  {
    auto next = std::chrono::steady_clock::now();
    Joints torque{};
    bool previous_torque_sent = false;
    uint64_t previous_command_ns = 0;
    State last_state = sm_.state();
    std::chrono::steady_clock::time_point last_bias_sample{};
    for (long tick = 0; running_ && rclcpp::ok(); ++tick) {
      next += std::chrono::microseconds(static_cast<int>(kLoopDt * 1e6));
      std::this_thread::sleep_until(next);
      RobotState s;
      const bool valid = read(s);
      const auto sample_time = std::chrono::steady_clock::now();
      const auto sample_stamp = now();
      const auto gravity = projected_gravity(s.quat_wxyz);
      sm_.observe(s.joint_pos, s.joint_vel, s.quat_wxyz, s.ang_vel, valid);
      handle_joystick(s, valid, torque);
      // Fault handling takes precedence over a joystick request in this tick.
      if (!valid || std::acos(std::clamp(-gravity[2], -1., 1.)) > kFallTilt) {
        sm_.request(State::Damp, s.joint_pos);
      }
      sm_.update(kLoopDt);
      const bool changed = sm_.state() != last_state;
      if (changed || sm_.state() != State::Rl) obs_builder_.reset();
      if (changed) RCLCPP_INFO(get_logger(), "state: %s", name(sm_.state()));
      last_state = sm_.state();
      if (obs_builder_.heading_enabled()) {
        sample_gyro_bias(s, valid);
        if (changed && sm_.state() == State::Rl) apply_gyro_bias();
        if (sm_.state() != State::Rl) last_heading_build_ = {};
      }

      if (sm_.state() != State::Rl) {
        std::fill(last_action_.begin(), last_action_.end(), 0.f);
        std::fill(applied_action_.begin(), applied_action_.end(), 0.f);
        leg_filter_.reset();
      }
      if (velocity_bias_ && sm_.state() != State::Rl) {
        velocity_bias_->reset();
        last_bias_sample = {};
      }
      const bool sample_now = tick % decimation_ == 0 || changed;
      const bool publish_now = sample_now && valid;
      tita_controller::msg::MotorFeedback feedback;
      if (sample_now) {
        feedback.previous_computed_torque = torque;
        feedback.previous_torque_sent = previous_torque_sent;
        feedback.previous_command_monotonic_ns = previous_command_ns;
        feedback.reported_torque.fill(std::numeric_limits<double>::quiet_NaN());
        try {
          const auto reported = robot_.get_joint_t();
          feedback.valid = !robot_.motors_data_timeout() && reported.size() == 8 &&
            std::all_of(reported.begin(), reported.end(), [](double x) {return std::isfinite(x);});
          if (feedback.valid) std::copy(reported.begin(), reported.end(), feedback.reported_torque.begin());
        } catch (const std::exception & e) {
          RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 1000, "torque feedback read failed: %s", e.what());
        }
        feedback.feedback_read_monotonic_ns = static_cast<uint64_t>(
          std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::steady_clock::now().time_since_epoch()).count());
      }
      bool policy_valid = false;
      std::vector<float> obs;
      if (publish_now) {
        try {
          // Heading integrates over the measured interval between RL observations (nominal policy_dt).
          double heading_dt = -1.;
          if (sm_.state() == State::Rl && obs_builder_.heading_enabled()) {
            if (last_heading_build_.time_since_epoch().count() != 0) {
              heading_dt = std::clamp(std::chrono::duration<double>(sample_time - last_heading_build_).count(),
                .25 * decimation_ * kLoopDt, 2.5 * decimation_ * kLoopDt);
            }
            last_heading_build_ = sample_time;
          }
          obs = obs_builder_.build(s, command_, last_action_, heading_dt);
          if (sm_.state() == State::Rl) {
            last_action_ = infer(obs);
            applied_action_ = leg_filter_.update(last_action_);
            policy_valid = true;
          }
          if (velocity_bias_ && sm_.state() == State::Rl) {
            const double dt = last_bias_sample.time_since_epoch().count() == 0 ? .02 :
              std::chrono::duration<double>(sample_time - last_bias_sample).count();
            const bool acquired = velocity_bias_->acquired();
            const bool inhibited = velocity_bias_->inhibited();
            velocity_bias_->update(s, command_, dt);
            if (!acquired && velocity_bias_->acquired()) {
              RCLCPP_INFO(get_logger(), "velocity bias acquired: drift=%.4f m/s, pitch_reference=%.4f rad",
                velocity_bias_->estimated_drift(), velocity_bias_->pitch_reference());
            }
            if (!inhibited && velocity_bias_->inhibited()) {
              RCLCPP_WARN(get_logger(), "velocity bias inhibited: acquisition/tilt/speed/pitch-deviation guard; "
                "correction OFF until command exit/reentry or RL reset");
            }
            last_bias_sample = sample_time;
          }
        } catch (const std::exception & e) {
          RCLCPP_ERROR(get_logger(), "policy failed, entering damp: %s", e.what());
          sm_.request(State::Damp, s.joint_pos);
          std::fill(last_action_.begin(), last_action_.end(), 0.f);
          std::fill(applied_action_.begin(), applied_action_.end(), 0.f);
          leg_filter_.reset();
          obs_builder_.reset();
          if (velocity_bias_) velocity_bias_->reset();
          last_bias_sample = {};
          obs.clear();
          policy_valid = false;
        }
      }
      const Joints baseline_torque = !valid ? Joints{} :
        sm_.state() == State::Rl ? action_adapter_.compute(applied_action_, s.joint_pos, s.joint_vel) :
        sm_.torque(s.joint_pos, s.joint_vel);
      torque = baseline_torque;
      if (valid && velocity_bias_ && sm_.state() == State::Rl) {
        torque = action_adapter_.compute(applied_action_, s.joint_pos, s.joint_vel,
          velocity_bias_->wheel_offsets());
      }
      bool sent = false;
      uint64_t command_ns = 0;
      if (output_enabled_) {
        try {
          sent = robot_.set_target_joint_t(std::vector<double>(torque.begin(), torque.end()));
        } catch (const std::exception & e) {
          RCLCPP_ERROR(get_logger(), "CAN torque transmission exception: %s", e.what());
        }
        command_ns = static_cast<uint64_t>(
          std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::steady_clock::now().time_since_epoch()).count());
        if (!sent) {
          output_enabled_ = false;
          policy_valid = false;
          sm_.request(State::Damp, s.joint_pos);
          std::fill(last_action_.begin(), last_action_.end(), 0.f);
          std::fill(applied_action_.begin(), applied_action_.end(), 0.f);
          leg_filter_.reset();
          if (velocity_bias_) velocity_bias_->reset();
          last_bias_sample = {};
          RCLCPP_ERROR(get_logger(),
            "CAN torque transmission failed; command output latched OFF. "
            "No further commands will be sent; motor torque release is NOT confirmed. "
            "Inspect CAN before restarting.");
        }
      }
      if (publish_now) publish(s, obs, torque, sample_stamp,
        {torque[3] - baseline_torque[3], torque[7] - baseline_torque[7]}, feedback);
      if (sample_now) publish_training(s, obs, torque, sample_stamp, sample_time,
        static_cast<uint64_t>(tick), valid, policy_valid, sent,
        {torque[3] - baseline_torque[3], torque[7] - baseline_torque[7]}, feedback);
      previous_torque_sent = sent;
      previous_command_ns = command_ns;
    }
  }

  std::vector<float> infer(std::vector<float> & obs)
  {
    const auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    const std::array<int64_t, 2> shape{1, static_cast<int64_t>(obs.size())};
    auto input = Ort::Value::CreateTensor<float>(memory, obs.data(), obs.size(), shape.data(), 2);
    Ort::AllocatorWithDefaultOptions allocator;
    const auto in_name = policy_->GetInputNameAllocated(0, allocator);
    const auto out_name = policy_->GetOutputNameAllocated(0, allocator);
    const char * in_names[] = {in_name.get()};
    const char * out_names[] = {out_name.get()};
    auto output = policy_->Run(Ort::RunOptions{nullptr}, in_names, &input, 1, out_names, 1);
    const float * data = output[0].GetTensorData<float>();
    if (!std::all_of(data, data + last_action_.size(), [](float x) {return std::isfinite(x);})) {
      throw std::runtime_error("non-finite policy action");
    }
    return std::vector<float>(data, data + last_action_.size());
  }

  void publish(const RobotState & s, const std::vector<float> & obs, const Joints & torque,
    const rclcpp::Time & stamp, const std::array<double, 2> & bias_torque,
    const tita_controller::msg::MotorFeedback & feedback)
  {
    sensor_msgs::msg::JointState joints;
    joints.header.stamp = stamp;
    joints.name = kJointNames;
    joints.position.assign(s.joint_pos.begin(), s.joint_pos.end());
    joints.velocity.assign(s.joint_vel.begin(), s.joint_vel.end());
    if (feedback.valid) joints.effort.assign(feedback.reported_torque.begin(), feedback.reported_torque.end());
    joint_pub_->publish(joints);
    sensor_msgs::msg::Imu imu;
    imu.header.stamp = joints.header.stamp;
    imu.orientation.w = s.quat_wxyz[0];
    imu.orientation.x = s.quat_wxyz[1];
    imu.orientation.y = s.quat_wxyz[2];
    imu.orientation.z = s.quat_wxyz[3];
    imu.angular_velocity.x = s.ang_vel[0];
    imu.angular_velocity.y = s.ang_vel[1];
    imu.angular_velocity.z = s.ang_vel[2];
    imu_pub_->publish(imu);
    std_msgs::msg::Float32MultiArray message;
    message.data = obs;
    obs_pub_->publish(message);
    message.data = last_action_;
    action_pub_->publish(message);
    message.data.assign(torque.begin(), torque.end());
    torque_pub_->publish(message);  // Native joint order, computed N*m before the output gate.
    message.data = velocity_bias_ ? velocity_bias_->diagnostics() : std::vector<float>(9, 0.f);
    message.data.push_back(static_cast<float>(bias_torque[0]));
    message.data.push_back(static_cast<float>(bias_torque[1]));
    bias_pub_->publish(message);
    std_msgs::msg::String state;
    state.data = name(sm_.state());
    state_pub_->publish(state);
  }

  void publish_training(const RobotState & s, const std::vector<float> & obs, const Joints & torque,
    const rclcpp::Time & stamp, std::chrono::steady_clock::time_point sample_time,
    uint64_t tick, bool valid, bool policy_valid, bool sent,
    const std::array<double, 2> & bias_torque, tita_controller::msg::MotorFeedback & feedback)
  {
    tita_controller::msg::TrainingSample sample;
    sample.header.stamp = stamp;
    sample.sequence_id = sample_sequence_++;
    sample.control_tick = tick;
    sample.monotonic_ns = static_cast<uint64_t>(
      std::chrono::duration_cast<std::chrono::nanoseconds>(sample_time.time_since_epoch()).count());
    sample.state = name(sm_.state());
    sample.sensors_valid = valid;
    sample.policy_valid = policy_valid;
    sample.output_enabled = output_enabled_;
    sample.torque_sent = sent;
    sample.command = command_;
    sample.observation = obs;
    std::copy(last_action_.begin(), last_action_.end(), sample.action_raw.begin());
    sample.wheel_velocity_bias = velocity_bias_ ? velocity_bias_->wheel_offsets() :
      std::array<double, 2>{};
    sample.teacher_action_valid = action_adapter_.teacher_action(
      applied_action_, sample.wheel_velocity_bias, sample.teacher_action) && policy_valid;
    sample.computed_torque = torque;
    sample.joint_position = s.joint_pos;
    sample.joint_velocity = s.joint_vel;
    sample.quaternion_wxyz = s.quat_wxyz;
    sample.angular_velocity = s.ang_vel;
    if (velocity_bias_) {
      const auto diagnostics = velocity_bias_->diagnostics();
      std::copy(diagnostics.begin(), diagnostics.end(), sample.velocity_bias_diagnostics.begin());
    }
    sample.velocity_bias_diagnostics[9] = static_cast<float>(bias_torque[0]);
    sample.velocity_bias_diagnostics[10] = static_cast<float>(bias_torque[1]);
    training_pub_->publish(sample);
    tita_controller::msg::ActionFilterSample filter;
    filter.header = sample.header;
    filter.sequence_id = sample.sequence_id;
    filter.control_tick = sample.control_tick;
    filter.monotonic_ns = sample.monotonic_ns;
    filter.leg_action_filter = leg_filter_.mode();
    std::copy(applied_action_.begin(), applied_action_.end(), filter.action_applied.begin());
    filter_pub_->publish(filter);
    feedback.header = sample.header;
    feedback.sequence_id = sample.sequence_id;
    feedback.control_tick = sample.control_tick;
    feedback.monotonic_ns = sample.monotonic_ns;
    feedback_pub_->publish(feedback);
  }

  StateMachine sm_;
  ObservationBuilder obs_builder_;
  ActionAdapter action_adapter_;
  LegActionFilter leg_filter_;
  std::unique_ptr<WheelVelocityBias> velocity_bias_;
  Ort::Env env_;
  std::unique_ptr<Ort::Session> policy_;
  tita_robot robot_;
  bool output_enabled_{false};
  double max_lin_x_{0.2}, max_ang_z_{0.3};
  double heading_bias_fallback_{0.};
  std::vector<double> gyro_samples_;
  std::size_t gyro_next_{0};
  std::chrono::steady_clock::time_point last_heading_build_{};
  int decimation_{10};
  int left_button_axis_{4}, right_button_axis_{6};
  std::array<double, 3> command_{};
  std::vector<float> last_action_;
  std::vector<float> applied_action_;
  uint64_t sample_sequence_{0};
  JoystickButtons buttons_;
  std::mutex joy_mutex_;
  sensor_msgs::msg::Joy joy_;
  std::chrono::steady_clock::time_point joy_time_{};
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_pub_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr obs_pub_, action_pub_, torque_pub_, bias_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr state_pub_;
  rclcpp::Publisher<tita_controller::msg::TrainingSample>::SharedPtr training_pub_;
  rclcpp::Publisher<tita_controller::msg::MotorFeedback>::SharedPtr feedback_pub_;
  rclcpp::Publisher<tita_controller::msg::ActionFilterSample>::SharedPtr filter_pub_;
  std::atomic_bool running_{true};
  std::thread loop_;
};
}  // namespace tita

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<tita::TitaNode>());
  rclcpp::shutdown();
}
