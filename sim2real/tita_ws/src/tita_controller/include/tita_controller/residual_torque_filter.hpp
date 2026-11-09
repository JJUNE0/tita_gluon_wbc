// 500 Hz residual-only filter; no inference, transport, allocation or ROS access.
#pragma once
#include "tita_controller/adapter.hpp"

namespace tita
{
class ResidualTorqueFilter
{
public:
  void configure(double cutoff_hz)
  {
    if (!std::isfinite(cutoff_hz) || cutoff_hz < 0. || cutoff_hz >= 250.)
      throw std::runtime_error("invalid residual LPF cutoff at 500 Hz");
    cutoff_hz_ = cutoff_hz;
    alpha_ = cutoff_hz == 0. ? 1. : -std::expm1(-2.*std::acos(-1.)*cutoff_hz*.002);
    reset();
  }
  void reset() {output_.fill(0.);}
  const Joints & update(const Joints & requested, bool valid)
  {
    if (!valid) {reset(); return output_;}
    for (std::size_t j = 0; j < output_.size(); ++j) {
      if (!std::isfinite(requested[j]) || std::abs(requested[j]) > 10.00001)
        throw std::runtime_error("invalid residual LPF request");
      output_[j] = cutoff_hz_ == 0. ? requested[j] : output_[j]+alpha_*(requested[j]-output_[j]);
    }
    return output_;
  }
  double cutoff_hz() const {return cutoff_hz_;}
private:
  double cutoff_hz_{0.}, alpha_{1.};
  Joints output_{};
};
}  // namespace tita
