// DESKTOP_DRY_RUN / ROBOT_COMMAND_FREE_RUNTIME: opt-in trained-pose residual gate.
#pragma once
#include <array>
#include <cmath>

namespace tita
{
struct ResidualPoseGateConfig
{
  bool allow_commands{false};
  std::array<double, 3> low{0., 0., .27};
  std::array<double, 3> high{0., 0., .42};
};

inline bool residual_pose_gate_valid(const ResidualPoseGateConfig & cfg)
{
  constexpr double roll = 0.5235987755982988, pitch = 0.2617993877991494;
  for (std::size_t i = 0; i < 3; ++i) {
    if (!std::isfinite(cfg.low[i]) || !std::isfinite(cfg.high[i]) || cfg.low[i] > cfg.high[i]) return false;
  }
  return cfg.low[0] >= -roll && cfg.high[0] <= roll && cfg.low[0] <= 0. && cfg.high[0] >= 0. &&
    cfg.low[1] >= -pitch && cfg.high[1] <= pitch && cfg.low[1] <= 0. && cfg.high[1] >= 0. &&
    cfg.low[2] >= .27 && cfg.high[2] <= .42;
}

inline bool residual_switch_enabled(double input) {return std::isfinite(input) && input == 0.;}

inline bool residual_stop_allowed(bool rl, const std::array<double, 3> & command,
  const std::array<double, 3> & target, const std::array<double, 3> & pose, bool pose_request_neutral,
  const ResidualPoseGateConfig & cfg = {})
{
  if (!rl || !residual_pose_gate_valid(cfg) || (!cfg.allow_commands && !pose_request_neutral)) return false;
  for (std::size_t i = 0; i < 3; ++i) {
    if (command[i] != 0. || target[i] != 0. || !std::isfinite(pose[i]) ||
      pose[i] < cfg.low[i] || pose[i] > cfg.high[i]) return false;
  }
  return cfg.allow_commands || (pose[0] == 0. && pose[1] == 0.);
}
}  // namespace tita
