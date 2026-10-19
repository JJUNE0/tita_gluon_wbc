// Update once per policy inference, then hold this action through the motor ticks.
#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace tita
{
class LegActionFilter
{
public:
  LegActionFilter(const std::string & mode, const std::vector<int64_t> & joint_order,
    double notch_hz = 8.3, double notch_q = 3.)
  : mode_(mode)
  {
    if (mode != "none" && mode != "ma2_legs" && mode != "ma2_notch_legs") {
      throw std::runtime_error("unknown leg_action_filter");
    }
    if (mode == "ma2_notch_legs") {
      if (!std::isfinite(notch_hz) || !std::isfinite(notch_q) ||
        notch_hz <= 0. || notch_hz >= 25. || notch_q <= 0. || notch_hz / notch_q >= 25.)
      {
        throw std::runtime_error("invalid notch frequency/Q/bandwidth at 50 Hz");
      }
      const double omega = 2. * std::acos(-1.) * notch_hz / 50.;
      b0_ = 1. / (1. + std::tan(omega / (2. * notch_q)));
      b1_ = -2. * b0_ * std::cos(omega);
      a2_ = 2. * b0_ - 1.;
    }
    if (joint_order.size() != 8) throw std::runtime_error("filter needs 8 action joints");
    std::array<bool, 8> seen{};
    for (std::size_t i = 0; i < 8; ++i) {
      const auto j = joint_order[i];
      if (j < 0 || j >= 8 || seen[j]) throw std::runtime_error("invalid filter joint mapping");
      seen[j] = true;
      legs_[i] = j != 3 && j != 7;
    }
  }

  void reset() {initialized_ = false;}
  const std::string & mode() const {return mode_;}

  std::vector<float> update(const std::vector<float> & raw)
  {
    if (raw.size() != 8 || !std::all_of(raw.begin(), raw.end(), [](float x) {return std::isfinite(x);})) {
      throw std::runtime_error("invalid leg filter action");
    }
    auto applied = raw;
    if (mode_ != "none" && initialized_) {
      for (std::size_t i = 0; i < 8; ++i) {
        if (legs_[i]) applied[i] = .5f * raw[i] + .5f * previous_[i];
      }
    }
    if (mode_ == "ma2_notch_legs") {
      for (std::size_t i = 0; i < 8; ++i) {
        if (!legs_[i]) continue;
        const double x = applied[i];
        if (!initialized_) {
          z1_[i] = (1. - b0_) * x;
          z2_[i] = (b0_ - a2_) * x;
        } else {
          const double y = b0_ * x + z1_[i];
          if (!std::isfinite(y) || std::abs(y) > std::numeric_limits<float>::max()) {
            throw std::runtime_error("non-finite leg notch output");
          }
          z1_[i] = b1_ * x - b1_ * y + z2_[i];
          z2_[i] = b0_ * x - a2_ * y;
          applied[i] = static_cast<float>(y);
        }
      }
    }
    std::copy(raw.begin(), raw.end(), previous_.begin());
    initialized_ = true;
    return applied;
  }

private:
  std::string mode_;
  std::array<bool, 8> legs_{};
  std::array<float, 8> previous_{};
  std::array<double, 8> z1_{}, z2_{};
  double b0_{1.}, b1_{0.}, a2_{0.};
  bool initialized_{false};
};
}  // namespace tita
