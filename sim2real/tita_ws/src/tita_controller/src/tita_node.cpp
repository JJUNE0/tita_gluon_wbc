// One control loop for policy, motors and joystick: same structure as sim2sim_node.py,
// with the MuJoCo env replaced by the TITA CAN API.
//
// Lower buttons: hold right >=1 s from idle -> transform_up; left down -> RL
// after sit; left up -> return_to_sit; a NEW right press -> latched supporting sit (faults use damping).
// Default left/right axes 4/6 follow the DDT two-position-channel convention;
// physical button mapping must be checked with motor output disabled.
// Sticks: axes[2] forward/back, axes[3] yaw; pose: -axes[0] roll, -axes[1] pitch, axes[5] height.

#include <atomic>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <limits>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "std_msgs/msg/string.hpp"
#include "tita_controller/adapter.hpp"
#include "tita_controller/control_loop_exit.hpp"
#include "tita_controller/motor_realtime.hpp"
#include "tita_controller/joystick_buttons.hpp"
#include "tita_controller/leg_action_filter.hpp"
#include "tita_controller/state_machine.hpp"
#include "tita_controller/msg/training_sample.hpp"
#include "tita_controller/msg/motor_feedback.hpp"
#include "tita_controller/msg/actuator_sample.hpp"
#include "tita_controller/actuator_capture.hpp"
#include "tita_controller/msg/action_filter_sample.hpp"
#include "tita_controller/velocity_bias.hpp"
#include "tita_controller/stop_residual.hpp"
#include "tita_controller/residual_torque_filter.hpp"
#include "tita_controller/learned_policy_engine.hpp"
#include "tita_controller/msg/policy_worker_sample.hpp"
#include "tita_robot/tita_robot.hpp"

namespace tita
{
constexpr double kLoopDt = 0.002;     // 500 Hz motor loop
constexpr double kFallTilt = 0.65;    // rad; beyond this -> damp
constexpr double kJoyTimeout = 0.5;   // s; stale joystick after enabling -> latched stop
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
      heading_config(), pose_config()),
    action_adapter_(action_terms(), joints("joint_kp"), joints("joint_kd"), joints("torque_limit")),
    leg_filter_(declare_parameter("leg_action_filter", std::string("none")),
      param<std::vector<int64_t>>("action_joint"),
      declare_parameter("leg_notch_hz", 8.3), declare_parameter("leg_notch_q", 3.)),
    env_(ORT_LOGGING_LEVEL_WARNING, "tita"),
    robot_(8)
  {
    output_enabled_ = declare_parameter("output_enabled", false);
    rcl_interfaces::msg::ParameterDescriptor scheduler_descriptor;
    scheduler_descriptor.read_only = true;
    motor_rt_priority_ = declare_parameter("motor_realtime_priority",
      motor_realtime_priority(std::getenv("TITA_MOTOR_RT_PRIORITY")), scheduler_descriptor);
    if (motor_rt_priority_ != 0 && motor_rt_priority_ != 20)
      throw std::runtime_error("motor_realtime_priority must be 20 or 0");
    rcl_interfaces::msg::ParameterDescriptor tilt_descriptor;
    tilt_descriptor.read_only = true;
    const double support_tilt_deg = declare_parameter("support_fall_tilt_deg", 55., tilt_descriptor);
    if (!std::isfinite(support_tilt_deg) || support_tilt_deg <= 0. || support_tilt_deg >= 90.) {
      throw std::runtime_error("support_fall_tilt_deg must be finite and between 0 and 90 degrees");
    }
    support_fall_tilt_ = support_tilt_deg * M_PI / 180.;
    support_mode_ = declare_parameter("support_mode", 2);
    if (support_mode_ < 0 || support_mode_ > 2) throw std::runtime_error("support_mode must be 0, 1 or 2");
    support_callback_ = add_on_set_parameters_callback([this](const std::vector<rclcpp::Parameter> & parameters) {
      rcl_interfaces::msg::SetParametersResult result;
      result.successful = true;
      for (const auto & parameter : parameters) {
        if (parameter.get_name() != "support_mode") continue;
        if (!obs_builder_.support_enabled() || parameter.get_type() != rclcpp::ParameterType::PARAMETER_INTEGER ||
          parameter.as_int() < 0 || parameter.as_int() > 2)
        {
          result.successful = false;
          result.reason = "support_mode needs a support-command policy and integer 0, 1 or 2";
          return result;
        }
      }
      return result;
    });
    const auto wheel_thresholds = get_parameter("wheel_position_velocity_thresholds").as_double_array();
    if (!wheel_thresholds.empty()) {
      wheel_odometry_ = std::make_unique<WheelKinematics>(
        param<std::vector<double>>("wheel_odometry_xyz"), param<std::vector<double>>("wheel_odometry_rpy"),
        param<std::vector<double>>("wheel_odometry_axis"), param<double>("wheel_position_radius"));
      RCLCPP_INFO(get_logger(), "wheel stop latch uses encoder/IMU contact kinematics; assumes requested support without slip");
    }
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
    if (obs_builder_.pose_enabled()) {
      pose_command_ = std::make_unique<PoseCommand>(pose_config());
      RCLCPP_INFO(get_logger(), "pose policy: right stick -axes[0] roll, -axes[1] pitch; "
        "height starts at %.3f m; axes[5] +/-1: +/-0.05 m/s, 0: hold; "
        "height speed overrides saved ramp; directions on hardware NOT_TESTED",
        pose_command_->value()[2]);
    }
    if (obs_builder_.support_enabled()) {
      RCLCPP_INFO(get_logger(), "support mode=%d (0 left, 1 right, 2 both); command caps vx=%.3f m/s, yaw=%.3f rad/s; "
        "RL total-tilt cutoff %.1f deg", support_mode_, max_lin_x_, max_ang_z_, support_tilt_deg);
    }
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
      if (obs_builder_.support_enabled()) throw std::runtime_error("velocity bias is not supported for support-command policies");
      if (obs_builder_.pose_enabled()) throw std::runtime_error("velocity bias is not supported for pose-command policies");
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
    std::shared_ptr<LearnedPolicyEngine> learned_engine;
    const auto residual_path = declare_parameter("residual_policy_path", std::string(""));
    residual_action_ = declare_parameter("residual_action_mode", false);
    const auto residual_lpf_hz = declare_parameter("residual_lpf_hz", 0.);
    const auto residual_shared_sensors = declare_parameter("residual_teacher_shared_sensors", false);
    residual_filter_.configure(residual_lpf_hz);
    if ((residual_lpf_hz > 0. || residual_shared_sensors) && (residual_path.empty() || residual_action_))
      throw std::runtime_error("saved torque residual required for LPF/shared sensors");
    residual_pose_gate_.allow_commands = declare_parameter("residual_allow_pose_commands", false);
    const auto pose_low = declare_parameter<std::vector<double>>("residual_pose_command_min", {0., 0., .27});
    const auto pose_high = declare_parameter<std::vector<double>>("residual_pose_command_max", {0., 0., .42});
    if (pose_low.size() != 3 || pose_high.size() != 3) throw std::runtime_error("residual pose gate requires three limits");
    std::copy(pose_low.begin(), pose_low.end(), residual_pose_gate_.low.begin());
    std::copy(pose_high.begin(), pose_high.end(), residual_pose_gate_.high.begin());
    if (!residual_pose_gate_valid(residual_pose_gate_)) throw std::runtime_error("invalid residual trained pose limits");

    if (!residual_path.empty()) {
      const double residual_dt = residual_action_ ? .02 : .004;
      if (velocity_bias_ || leg_filter_.mode() != "none" || !obs_builder_.pose_enabled() ||
        obs_size != 38 || decimation_ != 10 || std::abs(param<double>("observation_dt", .02) - residual_dt) > 1e-9)
      {
        throw std::runtime_error("stationary residual requires matched unfiltered Teacher38 and saved observation period");
      }
      if (residual_action_) {
        const auto ratios = param<std::vector<double>>("residual_action_to_policy", std::vector<double>(8, 0.));
        if (ratios.size() != 8 || !std::all_of(ratios.begin(), ratios.end(),
          [](double value) {return std::isfinite(value) && value > 0.;}))
        {
          throw std::runtime_error("invalid saved residual reference scales");
        }
        std::copy(ratios.begin(), ratios.end(), residual_action_to_policy_.begin());
        policy_bridge_ = PolicyMotorBridge(PolicyMotorBridge::kTeacherMaxAgeNs);
      }
      if (!wheel_odometry_) throw std::runtime_error("async residual requires saved wheel odometry geometry");
      const auto thresholds = param<std::vector<double>>("residual_wheel_velocity_thresholds", std::vector<double>{0., 0.});
      if (thresholds.size() != 2) throw std::runtime_error("residual latch requires two thresholds");
      const std::array<double, 2> residual_thresholds{thresholds[0], thresholds[1]};
      learned_engine = std::make_shared<LearnedPolicyEngine>(env_, std::move(policy_), residual_path,
        obs_builder_, *wheel_odometry_, residual_action_, residual_thresholds, residual_shared_sensors);
      RCLCPP_INFO(get_logger(), "residual LPF %.1f Hz at 500 Hz, residual-only before fresh PD sum; shared Teacher sensors=%s; history uses pre-filter request",
        residual_lpf_hz, residual_shared_sensors ? "true" : "false");
      if (thresholds[0] > 0.) RCLCPP_INFO(get_logger(),
        "residual wheel latch: encoder/IMU planar speed < %.3f m/s, raw yaw rate < %.3f rad/s; no dwell", thresholds[0], thresholds[1]);
      RCLCPP_WARN(get_logger(), "learned stop residual ON: %s, separate %.0f Hz worker, 500 Hz nonwaiting motor exchange; "
        "residual expires at %.0f ms, Teacher/startup at 40 ms; zero velocity command and axes[7]=0; pose_gate=%s; hardware NOT_TESTED",
        residual_action_ ? "normalized joint reference correction" : "torque correction +/-10 Nm",
        1./residual_dt, residual_action_ ? 40. : 12., residual_pose_gate_.allow_commands ? "trained_pose_range" : "neutral_roll_pitch");
    }

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
    if (learned_engine) {
      residual_pub_ = create_publisher<std_msgs::msg::Float32MultiArray>(
        residual_action_ ? "/sim2real/debug/residual_action" : "/sim2real/debug/residual", 10);
      worker_pub_ = create_publisher<tita_controller::msg::PolicyWorkerSample>("/sim2real/policy_worker_sample", 10);
      async_policy_ = std::make_unique<AsyncPolicyWorker>(
        [learned_engine](const PolicyInput & input) {return learned_engine->step(input);},
        [this](const PolicyOutput & output) {publish_worker(output);},
        std::chrono::microseconds(residual_action_ ? 20000 : 4000));
    }
    state_pub_ = create_publisher<std_msgs::msg::String>("/sim2real/debug/state", 10);
    training_pub_ = create_publisher<tita_controller::msg::TrainingSample>("/sim2real/training_sample", 10);
    feedback_pub_ = create_publisher<tita_controller::msg::MotorFeedback>("/sim2real/motor_feedback", 10);
    filter_pub_ = create_publisher<tita_controller::msg::ActionFilterSample>("/sim2real/action_filter_sample", 10);
    if (declare_parameter("actuator_logging", false)) {
      capture_pub_ = create_publisher<tita_controller::msg::ActuatorSample>(
        "/sim2real/actuator_sample", rclcpp::QoS(2048).reliable());
      capture_ = std::make_unique<ActuatorCapture>([this](const ActuatorRecord & r) {publish_capture(r);});
      RCLCPP_INFO(get_logger(), "500 Hz actuator capture ON: bounded 2048-snapshot queue, separate publisher; SDK cached feedback, no CAN acquisition timestamp");
    }
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
        [this] {
          ScopedMotorRealtime<> scheduling(output_enabled_, motor_rt_priority_);
          if (scheduling.active()) {
            RCLCPP_INFO(get_logger(), "motor thread scheduling ACTIVE: SCHED_FIFO priority20, timer_slack=1 ns; "
              "synchronous SDK TX, original 100 us frame waits; policy/receive/publisher thread scheduling unchanged");
          } else {
            RCLCPP_INFO(get_logger(), "motor thread scheduling unchanged: output_enabled=%s, motor_realtime_priority=%d",
              output_enabled_ ? "true" : "false", motor_rt_priority_);
          }
          run();
        }, output_enabled_,
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
    if (async_policy_) async_policy_->stop();
    if (capture_) {
      capture_->stop();
      RCLCPP_INFO(get_logger(), "actuator capture: accepted=%llu published=%llu queue_dropped=%llu publish_errors=%llu; bag delivery checked offline",
        static_cast<unsigned long long>(capture_->accepted()), static_cast<unsigned long long>(capture_->published()),
        static_cast<unsigned long long>(capture_->dropped()), static_cast<unsigned long long>(capture_->errors()));
    }
  }

private:
  // Required parameter (set by tita.launch.py); safe to read more than once.
  template<class T>
  T param(const std::string & name)
  {
    if (!has_parameter(name)) declare_parameter<T>(name);
    return get_parameter(name).get_value<T>();
  }

  template<class T>
  T param(const std::string & name, const T & fallback)
  {
    if (!has_parameter(name)) declare_parameter<T>(name, fallback);
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
    const auto speeds = declare_parameter("wheel_position_velocity_thresholds", std::vector<double>{});
    if (!speeds.empty()) {
      if (speeds.size() != 2) throw std::runtime_error("wheel position velocity thresholds need 2 values");
      std::copy(speeds.begin(), speeds.end(), cfg.velocity_thresholds.begin());
      cfg.velocity_gated = true;
    }
    cfg.moving_anchor = declare_parameter("wheel_position_moving_anchor", false);
    return cfg;
  }

  HeadingConfig heading_config()
  {
    HeadingConfig cfg;
    cfg.clip_rad = declare_parameter("heading_clip_rad", 0.);
    cfg.warmup_s = declare_parameter("heading_warmup_s", 0.);
    cfg.dt = param<double>("observation_dt", param<double>("policy_dt"));
    const auto thresholds = declare_parameter("heading_zero_thresholds", std::vector<double>{0., 0., 0.});
    if (thresholds.size() != 3) throw std::runtime_error("heading zero thresholds need 3 values");
    std::copy(thresholds.begin(), thresholds.end(), cfg.zero_thresholds.begin());
    return cfg;
  }

  PoseCommandConfig pose_config()
  {
    PoseCommandConfig cfg;
    const auto low = param<std::vector<double>>("pose_low", std::vector<double>{0., 0., .335});
    const auto high = param<std::vector<double>>("pose_high", std::vector<double>{0., 0., .335});
    const auto rates = param<std::vector<double>>("pose_ramp_rates", std::vector<double>{.15, .15, .02});
    cfg.nominal_height = param<double>("pose_nominal_height", .335);
    if (low.size() != 3 || high.size() != 3 || rates.size() != 3) {
      throw std::runtime_error("pose ranges/ramp rates need 3 values");
    }
    std::copy(low.begin(), low.end(), cfg.low.begin());
    std::copy(high.begin(), high.end(), cfg.high.begin());
    std::copy(rates.begin(), rates.end(), cfg.rates.begin());
    cfg.validate();
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
    if (pose_command_) {
      const bool active = valid && sensors_valid && sm_.state() == State::Rl;
      pose_command_->update(active ? joy.axes[0] : 0., active ? joy.axes[1] : 0., active, kLoopDt,
        active ? joy.axes[5] : 0.);
    }
    command_target_ = target;
    height_input_ = valid ? joy.axes[5] : std::numeric_limits<double>::quiet_NaN();
    residual_switch_input_ = valid && joy.axes.size() > 7 ? joy.axes[7] : std::numeric_limits<double>::quiet_NaN();
    pose_request_neutral_ = valid && joy.axes[0] == 0.f && joy.axes[1] == 0.f;
    if (sm_.state() != State::Rl) {
      command_.fill(0.);
      return;
    }
    command_ = target;
  }

  void run()
  {
    auto next = std::chrono::steady_clock::now();
    Joints torque{};
    bool previous_torque_sent = false;
    uint64_t previous_command_ns = 0;
    State last_state = sm_.state();
    std::chrono::steady_clock::time_point last_bias_sample{};
    auto previous_loop_time = next;
    std::chrono::steady_clock::time_point previous_residual_sample{};
    long residual_phase = 0;
    SynchronousCaptureTrace synchronous_trace;
    for (long tick = 0; running_ && rclcpp::ok(); ++tick) {
      next += std::chrono::microseconds(static_cast<int>(kLoopDt * 1e6));
      std::this_thread::sleep_until(next);
      const uint64_t read_begin_ns = capture_ ? policy_now_ns() : 0;
      RobotState s;
      const bool valid = read(s);
      const auto sample_time = std::chrono::steady_clock::now();
      const double loop_us = std::chrono::duration<double, std::micro>(sample_time - previous_loop_time).count();
      previous_loop_time = sample_time;
      const auto sample_stamp = now();
      sm_.observe(s.joint_pos, s.joint_vel, s.quat_wxyz, s.ang_vel, valid);
      handle_joystick(s, valid, torque);
      // Fault handling takes precedence over a joystick request in this tick.
      const double tilt_limit = sm_.state() == State::Rl && obs_builder_.support_enabled() ? support_fall_tilt_ : kFallTilt;
      if (!valid || exceeds_fall_tilt(s.quat_wxyz, tilt_limit)) {
        sm_.request(State::Damp, s.joint_pos);
      }
      sm_.update(kLoopDt);
      const bool changed = sm_.state() != last_state;
      if (changed) residual_phase = 0;
      if (changed && async_policy_) {
        ++policy_epoch_;
        policy_bridge_.begin(policy_epoch_, policy_now_ns());
      }
      if (changed || sm_.state() != State::Rl) obs_builder_.reset();
      if (changed) RCLCPP_INFO(get_logger(), "state: %s", name(sm_.state()));
      last_state = sm_.state();
      if (obs_builder_.heading_enabled()) {
        sample_gyro_bias(s, valid);
        if (changed && sm_.state() == State::Rl) apply_gyro_bias();
        if (sm_.state() != State::Rl) last_heading_build_ = {};
      }

      if (sm_.state() != State::Rl) {
        if (pose_command_) pose_command_->reset();
        std::fill(last_action_.begin(), last_action_.end(), 0.f);
        std::fill(applied_action_.begin(), applied_action_.end(), 0.f);
        leg_filter_.reset();
      }
      if (velocity_bias_ && sm_.state() != State::Rl) {
        velocity_bias_->reset();
        last_bias_sample = {};
      }
      const bool sample_now = (async_policy_ ? residual_phase : tick) % decimation_ == 0 || changed;
      const bool observation_now = sample_now || (async_policy_ && sm_.state() == State::Rl &&
        residual_phase % (residual_action_ ? 10 : 2) == 0);
      const auto pose = pose_command_ ? pose_command_->value() : std::array<double, 3>{0., 0., .335};
      const bool residual_allowed = async_policy_ && valid && residual_switch_enabled(residual_switch_input_) && residual_stop_allowed(
        sm_.state() == State::Rl, command_, command_target_, pose, pose_request_neutral_, residual_pose_gate_);
      if (async_policy_ && (changed || residual_allowed != previous_residual_allowed_)) {
        RCLCPP_INFO(get_logger(), "residual gate %s: state=%s, enable_switch(axes[7])=%+.3f, height_input(axes[5])=%+.3f, height_target=%.4f, "
          "roll=%.4f, pitch=%.4f, command=[%.4f,%.4f,%.4f]; axes[7]=0; pose_gate=%s",
          residual_allowed ? "ON" : "OFF", name(sm_.state()), residual_switch_input_, height_input_, pose[2], pose[0], pose[1],
          command_[0], command_[1], command_[2], residual_pose_gate_.allow_commands ? "trained_pose_range" : "neutral_roll_pitch");
      }
      if (residual_allowed != previous_residual_allowed_) {
        ++residual_epoch_;
        previous_residual_allowed_ = residual_allowed;
      }
      const bool publish_now = sample_now && valid;
      tita_controller::msg::MotorFeedback feedback;
      if (sample_now || capture_) {
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
      double residual_inference_us = 0.;
      PolicyDecision decision;
      selected_residual_.fill(0.);
      selected_residual_valid_ = false;
      if (async_policy_) {
        PolicyOutput output;
        if (async_policy_->poll(output)) policy_bridge_.accept(output);
        decision = policy_bridge_.decide(policy_now_ns(), residual_epoch_,
          valid && sm_.state() == State::Rl, residual_allowed, async_policy_->failed());
        if (decision.fault) {
          RCLCPP_ERROR(get_logger(), "async policy stale/failed, entering damp: %s",
            async_policy_->failed() ? async_policy_->error().c_str() : "Teacher result older than 40 ms or startup timeout");
          sm_.request(State::Damp, s.joint_pos);
          std::fill(last_action_.begin(), last_action_.end(), 0.f);
          std::fill(applied_action_.begin(), applied_action_.end(), 0.f);
        } else if (decision.valid) {
          last_action_.assign(decision.action.begin(), decision.action.end());
          applied_action_ = last_action_;  // Filtered policies are rejected with this residual.
          selected_residual_ = decision.residual;
          selected_residual_valid_ = decision.residual_valid;
          if (residual_action_) {
            for (std::size_t j = 0; j < 8; ++j) {
              applied_action_[j] += selected_residual_[j]*residual_action_to_policy_[j];
            }
          }
          if (decision.residual_valid && reported_active_epoch_ != residual_epoch_) {
            reported_active_epoch_ = residual_epoch_;
            RCLCPP_INFO(get_logger(), "residual ACTIVE: height_target=%.4f, source_age=%.3f ms, stop_epoch=%llu",
              pose[2], (policy_now_ns()-policy_bridge_.output()->source.sensed_ns)*1e-6,
              static_cast<unsigned long long>(residual_epoch_));
          }
          const auto * result = policy_bridge_.output();
          if (sample_now) obs.assign(result->observation.begin(), result->observation.end());
          residual_inference_us = result->residual_us;
          policy_valid = sm_.state() == State::Rl;
        }
        // Publish the newest sensor/command snapshot without waiting for the worker.
        PolicyInput input;
        input.state = s;
        input.state.pose_command = pose;
        input.command = command_;
        std::copy(applied_action_.begin(), applied_action_.end(), input.applied_action.begin());
        input.applied_residual = selected_residual_;  // Requested pre-LPF feedback, as trained.
        input.control_tick = static_cast<uint64_t>(tick);
        input.sensed_ns = static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(sample_time.time_since_epoch()).count());
        input.epoch = policy_epoch_;
        input.stop_epoch = residual_epoch_;
        input.gyro_bias = obs_builder_.gyro_bias();
        input.rl = valid && sm_.state() == State::Rl;
        input.stop_allowed = input.rl && residual_allowed;
        async_policy_->submit(input);
      }
      if (!async_policy_ && observation_now && valid) {
        try {
          // Heading integrates over the measured interval between RL observations (nominal policy_dt).
          s.support_mode = static_cast<int>(get_parameter("support_mode").as_int());
          if (s.support_mode != support_mode_) {
            support_mode_ = s.support_mode;
            RCLCPP_INFO(get_logger(), "support mode: %d (0 left, 1 right, 2 both)", support_mode_);
          }
          if (wheel_odometry_) s.lin_vel_b = wheel_odometry_->linear_velocity(s);
          if (pose_command_) s.pose_command = pose_command_->value();
          double heading_dt = -1.;
          if (sm_.state() == State::Rl && obs_builder_.heading_enabled()) {
            if (last_heading_build_.time_since_epoch().count() != 0) {
              const double period = decimation_ * kLoopDt;
              heading_dt = std::clamp(std::chrono::duration<double>(sample_time - last_heading_build_).count(),
                .25 * period, 2.5 * period);
            }
            last_heading_build_ = sample_time;
          }
          obs = obs_builder_.build(s, command_, last_action_, heading_dt);
          if (sample_now && sm_.state() == State::Rl) {
            if (capture_) synchronous_trace.started_ns = policy_now_ns();
            last_action_ = infer(obs);
            if (capture_) {
              synchronous_trace.complete(static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(sample_time.time_since_epoch()).count()), policy_now_ns());
            }
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
          if (pose_command_) pose_command_->reset();
          if (velocity_bias_) velocity_bias_->reset();
          last_bias_sample = {};
          obs.clear();
          policy_valid = false;
        }
      }
      const Joints baseline_torque = !valid ? Joints{} :
        sm_.state() == State::Rl ? (decision.pending ? torque : action_adapter_.compute(applied_action_, s.joint_pos, s.joint_vel)) :
        sm_.torque(s.joint_pos, s.joint_vel);
      torque = baseline_torque;
      const auto filtered_residual = residual_filter_.update(selected_residual_,
        valid && async_policy_ && !residual_action_ && decision.valid && decision.residual_valid &&
        residual_allowed && sm_.state() == State::Rl);
      if (valid && async_policy_ && !residual_action_ && decision.valid && sm_.state() == State::Rl) {
        torque = action_adapter_.compute(applied_action_, s.joint_pos, s.joint_vel, {}, filtered_residual);
      }
      if (valid && velocity_bias_ && sm_.state() == State::Rl) {
        torque = action_adapter_.compute(applied_action_, s.joint_pos, s.joint_vel,
          velocity_bias_->wheel_offsets());
      }
      bool sent = false;
      uint64_t command_ns = 0;
      const uint64_t command_begin_ns = output_enabled_ && capture_ ? policy_now_ns() : 0;
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
          selected_residual_.fill(0.);
          selected_residual_valid_ = false;
          residual_filter_.reset();
          last_bias_sample = {};
          RCLCPP_ERROR(get_logger(),
            "CAN torque transmission failed; command output latched OFF. "
            "No further commands will be sent; motor torque release is NOT confirmed. "
            "Inspect CAN before restarting.");
        }
      }
      if (async_policy_ && observation_now) {
        const double residual_period_us = previous_residual_sample.time_since_epoch().count() == 0 ? 0. :
          std::chrono::duration<double, std::micro>(sample_time - previous_residual_sample).count();
        previous_residual_sample = sample_time;
        std_msgs::msg::Float32MultiArray debug;
        debug.data = {decision.residual_valid && sm_.state() == State::Rl ? 1.f : 0.f,
          static_cast<float>(residual_inference_us), static_cast<float>(loop_us),
          static_cast<float>(std::max(0., std::chrono::duration<double, std::micro>(
            std::chrono::steady_clock::now() - (next + std::chrono::microseconds(2000))).count())),
          static_cast<float>(residual_period_us)};
        for (double x : selected_residual_) debug.data.push_back(static_cast<float>(x));
        for (double x : torque) debug.data.push_back(static_cast<float>(x));
        residual_pub_->publish(debug);
      }
      ++residual_phase;
      const std::array<double, 2> bias_torque = velocity_bias_ ?
        std::array<double, 2>{torque[3] - baseline_torque[3], torque[7] - baseline_torque[7]} :
        std::array<double, 2>{};
      if (publish_now) publish(s, obs, torque, sample_stamp,
        bias_torque, feedback);
      if (sample_now) publish_training(s, obs, torque, sample_stamp, sample_time,
        static_cast<uint64_t>(tick), valid, policy_valid, sent,
        bias_torque, feedback);
      if (capture_) {
        synchronous_trace.observe_rl(valid && sm_.state() == State::Rl);
        ActuatorRecord r;
        r.ros_ns = sample_stamp.nanoseconds(); r.sequence = capture_sequence_++; r.tick = tick;
        r.sensed_ns = static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(sample_time.time_since_epoch()).count());
        r.read_begin_ns = read_begin_ns; r.feedback_read_ns = feedback.feedback_read_monotonic_ns;
        r.command_begin_ns = command_begin_ns; r.command_end_ns = command_ns;
        r.previous_command_ns = feedback.previous_command_monotonic_ns;
        r.dropped = capture_->dropped(); r.loop_us = loop_us;
        r.deadline_late_us = std::max(0., std::chrono::duration<double, std::micro>(
          std::chrono::steady_clock::now()-(next+std::chrono::microseconds(2000))).count());
        r.state = static_cast<uint8_t>(sm_.state()); r.sensors_valid = valid; r.feedback_valid = feedback.valid;
        r.policy_valid = async_policy_ ? policy_valid : synchronous_trace.valid;
        r.reference_valid = r.policy_valid && valid && sm_.state() == State::Rl;
        r.output_enabled = output_enabled_; r.sent = sent; r.previous_sent = feedback.previous_torque_sent;
        r.asynchronous = static_cast<bool>(async_policy_); r.residual_valid = selected_residual_valid_ && sm_.state() == State::Rl;
        r.residual_action = residual_action_; r.residual_allowed = residual_allowed;
        r.q = s.joint_pos; r.dq = s.joint_vel; r.quat = s.quat_wxyz; r.gyro = s.ang_vel;
        r.command = command_; r.pose = pose; r.torque = torque; r.reported = feedback.reported_torque;
        r.previous_torque = feedback.previous_computed_torque; r.residual = selected_residual_;
        r.filtered_residual = filtered_residual;
        r.residual_lpf_hz = residual_filter_.cutoff_hz();
        r.kp = action_adapter_.kp(); r.kd = action_adapter_.kd(); r.limits = action_adapter_.effort_limits();
        std::copy(last_action_.begin(), last_action_.end(), r.teacher_action.begin());
        std::copy(applied_action_.begin(), applied_action_.end(), r.applied_action.begin());
        r.reference_q.fill(NAN); r.reference_dq.fill(NAN);
        if (r.reference_valid) action_adapter_.reference_targets(applied_action_,
          velocity_bias_ ? velocity_bias_->wheel_offsets() : std::array<double, 2>{}, r.reference_q, r.reference_dq);
        r.policy_epoch = policy_epoch_; r.residual_epoch = residual_epoch_;
        if (async_policy_ && policy_bridge_.output()) {
          const auto & result = *policy_bridge_.output();
          r.policy_sequence = result.sequence; r.policy_source_ns = result.source.sensed_ns;
          r.teacher_source_ns = result.teacher_source_ns;
          r.policy_started_ns = result.started_ns; r.policy_completed_ns = result.completed_ns;
        } else if (!async_policy_) {
          r.policy_source_ns = r.teacher_source_ns = synchronous_trace.source_ns;
          r.policy_started_ns = synchronous_trace.started_ns; r.policy_completed_ns = synchronous_trace.completed_ns;
        }
        capture_->push(r);  // Fixed-size copy only; never waits for ROS or disk.
      }
      previous_torque_sent = sent;
      previous_command_ns = command_ns;
    }
  }

  void publish_capture(const ActuatorRecord & r)
  {
    tita_controller::msg::ActuatorSample m;
    m.header.stamp = rclcpp::Time(r.ros_ns);
    m.sequence_id = r.sequence; m.control_tick = r.tick; m.monotonic_ns = r.sensed_ns;
    m.sensor_read_begin_monotonic_ns = r.read_begin_ns; m.feedback_read_monotonic_ns = r.feedback_read_ns;
    m.command_begin_monotonic_ns = r.command_begin_ns; m.command_return_monotonic_ns = r.command_end_ns;
    m.previous_command_monotonic_ns = r.previous_command_ns; m.capture_dropped_total = r.dropped;
    m.loop_interval_us = r.loop_us; m.next_deadline_lateness_us = r.deadline_late_us;
    m.state = r.state; m.sensors_valid = r.sensors_valid; m.feedback_valid = r.feedback_valid;
    m.policy_valid = r.policy_valid; m.reference_valid = r.reference_valid; m.output_enabled = r.output_enabled;
    m.torque_sent = r.sent; m.previous_torque_sent = r.previous_sent; m.asynchronous_policy = r.asynchronous;
    m.residual_result_valid = r.residual_valid; m.residual_is_action = r.residual_action; m.residual_allowed = r.residual_allowed;
    m.policy_worker_sequence = r.policy_sequence; m.policy_source_monotonic_ns = r.policy_source_ns;
    m.teacher_source_monotonic_ns = r.teacher_source_ns; m.policy_epoch = r.policy_epoch; m.residual_epoch = r.residual_epoch;
    m.policy_started_monotonic_ns = r.policy_started_ns; m.policy_completed_monotonic_ns = r.policy_completed_ns;
    m.joint_position = r.q; m.joint_velocity = r.dq; m.reference_position = r.reference_q; m.reference_velocity = r.reference_dq;
    m.joint_kp = r.kp; m.joint_kd = r.kd; m.effort_limit = r.limits;
    m.computed_torque = r.torque; m.reported_torque = r.reported; m.previous_computed_torque = r.previous_torque;
    m.teacher_action = r.teacher_action; m.applied_action = r.applied_action; m.selected_residual = r.residual;
    m.filtered_residual = r.filtered_residual; m.residual_lpf_hz = r.residual_lpf_hz;
    m.quaternion_wxyz = r.quat; m.angular_velocity = r.gyro; m.command = r.command; m.pose_command = r.pose;
    capture_pub_->publish(m);
  }

  void publish_worker(const PolicyOutput & output)
  {
    tita_controller::msg::PolicyWorkerSample sample;
    sample.sequence_id = output.sequence;
    sample.epoch = output.source.epoch;
    sample.residual_epoch = output.source.stop_epoch;
    sample.source_control_tick = output.source.control_tick;
    sample.source_monotonic_ns = output.source.sensed_ns;
    sample.started_monotonic_ns = output.started_ns;
    sample.completed_monotonic_ns = output.completed_ns;
    sample.teacher_source_control_tick = output.teacher_source_tick;
    sample.teacher_source_monotonic_ns = output.teacher_source_ns;
    sample.rl = output.source.rl;
    sample.residual_allowed = output.source.stop_allowed;
    sample.residual_is_action = residual_action_;
    sample.teacher_updated = output.teacher_updated;
    sample.residual_updated = output.residual_updated;
    sample.observation_us = output.observation_us;
    sample.teacher_us = output.teacher_us;
    sample.residual_us = output.residual_us;
    sample.joint_position = output.source.state.joint_pos;
    sample.joint_velocity = output.source.state.joint_vel;
    sample.quaternion_wxyz = output.source.state.quat_wxyz;
    sample.angular_velocity = output.source.state.ang_vel;
    sample.command = output.source.command;
    sample.pose_command = output.source.state.pose_command;
    sample.previously_selected_action = output.source.applied_action;
    sample.previously_selected_residual = output.source.applied_residual;
    sample.observation = output.observation;
    sample.teacher_action = output.action;
    sample.requested_residual = output.residual;
    sample.latch_velocity_estimate = output.latch_velocity_estimate;
    sample.residual_position_latched = output.residual_position_latched;
    sample.residual_wheel_position_error_m = output.residual_wheel_position_error_m;
    worker_pub_->publish(sample);  // Logging stays on the worker, never under an exchange lock.
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
    sample.residual_is_action = residual_action_;
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
    sample.asynchronous_policy = static_cast<bool>(async_policy_);
    sample.policy_epoch = policy_epoch_;
    sample.residual_epoch = residual_epoch_;
    if (async_policy_ && policy_bridge_.output()) {
      const auto & result = *policy_bridge_.output();
      sample.policy_worker_sequence = result.sequence;
      sample.policy_source_control_tick = result.source.control_tick;
      sample.policy_source_monotonic_ns = result.source.sensed_ns;
      sample.teacher_source_monotonic_ns = result.teacher_source_ns;
      const uint64_t clock_ns = policy_now_ns();
      sample.policy_result_age_ms = clock_ns >= result.source.sensed_ns ? (clock_ns-result.source.sensed_ns)*1e-6 : -1.;
      sample.residual_result_valid = selected_residual_valid_ && sm_.state() == State::Rl;
    }
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
  std::unique_ptr<WheelKinematics> wheel_odometry_;
  std::unique_ptr<PoseCommand> pose_command_;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr support_callback_;
  Ort::Env env_;
  std::unique_ptr<Ort::Session> policy_;
  tita_robot robot_;
  bool output_enabled_{false};
  int motor_rt_priority_{20};
  double max_lin_x_{0.2}, max_ang_z_{0.3};
  double support_fall_tilt_{0.};
  double heading_bias_fallback_{0.};
  std::vector<double> gyro_samples_;
  std::size_t gyro_next_{0};
  std::chrono::steady_clock::time_point last_heading_build_{};
  int decimation_{10};
  int left_button_axis_{4}, right_button_axis_{6};
  int support_mode_{2};
  std::array<double, 3> command_{};
  std::array<double, 3> command_target_{};
  bool pose_request_neutral_{false};
  ResidualPoseGateConfig residual_pose_gate_{};
  double height_input_{std::numeric_limits<double>::quiet_NaN()};
  double residual_switch_input_{std::numeric_limits<double>::quiet_NaN()};
  PolicyMotorBridge policy_bridge_;
  uint64_t policy_epoch_{0}, residual_epoch_{0};
  uint64_t reported_active_epoch_{std::numeric_limits<uint64_t>::max()};
  bool previous_residual_allowed_{false};
  Joints selected_residual_{};
  ResidualTorqueFilter residual_filter_;
  Joints residual_action_to_policy_{};
  bool residual_action_{false};
  bool selected_residual_valid_{false};
  std::vector<float> last_action_;
  std::vector<float> applied_action_;
  uint64_t sample_sequence_{0};
  uint64_t capture_sequence_{0};
  rclcpp::Publisher<tita_controller::msg::ActuatorSample>::SharedPtr capture_pub_;
  std::unique_ptr<ActuatorCapture> capture_;
  JoystickButtons buttons_;
  std::mutex joy_mutex_;
  sensor_msgs::msg::Joy joy_;
  std::chrono::steady_clock::time_point joy_time_{};
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_pub_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr obs_pub_, action_pub_, torque_pub_, bias_pub_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr residual_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr state_pub_;
  rclcpp::Publisher<tita_controller::msg::TrainingSample>::SharedPtr training_pub_;
  rclcpp::Publisher<tita_controller::msg::MotorFeedback>::SharedPtr feedback_pub_;
  rclcpp::Publisher<tita_controller::msg::ActionFilterSample>::SharedPtr filter_pub_;
  rclcpp::Publisher<tita_controller::msg::PolicyWorkerSample>::SharedPtr worker_pub_;
  std::atomic_bool running_{true};
  std::unique_ptr<AsyncPolicyWorker> async_policy_;
  std::thread loop_;
};
}  // namespace tita

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<tita::TitaNode>());
  rclcpp::shutdown();
}
