// Pose-policy commands: right stick sets roll/pitch; axes[5] integrates height at 5 cm/s.
#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <stdexcept>

namespace tita
{
struct PoseCommandConfig
{
  std::array<double, 3> low{0., 0., .335}, high{0., 0., .335};
  std::array<double, 3> rates{.15, .15, .02};
  double nominal_height{.335};

  void validate() const
  {
    for (std::size_t i = 0; i < 3; ++i) {
      if (!std::isfinite(low[i]) || !std::isfinite(high[i]) || low[i] > high[i] ||
        !std::isfinite(rates[i]) || rates[i] <= 0.)
      {
        throw std::runtime_error("invalid pose command ranges/ramp rates");
      }
    }
    if (low[0] < -M_PI/2 || high[0] > M_PI/2 || low[1] < -M_PI/2 || high[1] > M_PI/2 ||
      low[0] > 0. || high[0] < 0. || low[1] > 0. || high[1] < 0. ||
      low[2] <= 0. || !std::isfinite(nominal_height) ||
      nominal_height < low[2] || nominal_height > high[2])
    {
      throw std::runtime_error("invalid pose command nominal/ranges");
    }
  }
};

class PoseCommand
{
public:
  explicit PoseCommand(PoseCommandConfig cfg) : cfg_(cfg) {cfg_.validate(); reset();}

  void reset() {value_ = {0., 0., cfg_.nominal_height};}

  void update(double right_x, double right_y, bool active, double dt, double height_switch = 0.)
  {
    if (!active) {reset(); return;}
    if (!std::isfinite(right_x) || !std::isfinite(right_y) || !std::isfinite(height_switch) ||
      !std::isfinite(dt) || dt <= 0.)
    {
      throw std::runtime_error("invalid pose joystick inputs");
    }
    const std::array<double, 2> stick{-std::clamp(right_x, -1., 1.), -std::clamp(right_y, -1., 1.)};
    for (std::size_t i = 0; i < 2; ++i) {
      const double target = std::abs(stick[i]) * (stick[i] < 0. ? cfg_.low[i] : cfg_.high[i]);
      value_[i] += std::clamp(target - value_[i], -cfg_.rates[i] * dt, cfg_.rates[i] * dt);
      value_[i] = std::clamp(value_[i], cfg_.low[i], cfg_.high[i]);
    }
    // Operator-selected 0.05 m/s overrides the export's 0.02 m/s height ramp.
    // Neutral holds the current height; clipping prevents accumulation past either bound.
    const double direction = height_switch >= .5 ? 1. : height_switch <= -.5 ? -1. : 0.;
    value_[2] = std::clamp(value_[2] + direction * .05 * dt, cfg_.low[2], cfg_.high[2]);
  }

  const std::array<double, 3> & value() const {return value_;}

private:
  PoseCommandConfig cfg_;
  std::array<double, 3> value_{};
};
}  // namespace tita
