// Left latching selector; right holds for startup and presses once to latch stop.
#pragma once

#include <cmath>
#include <optional>

namespace tita
{
enum class ButtonEvent { None, TransformUp, Rl, ReturnToSit, Stop };

inline std::optional<bool> button_down(double value)
{
  if (!std::isfinite(value) || std::abs(value) > 1.1) return std::nullopt;
  if (value <= -.5) return true;
  if (value >= .5) return false;
  return std::nullopt;  // Middle/unknown is not a valid latching-button position.
}

class JoystickButtons
{
public:
  ButtonEvent update(bool valid, bool left_down, bool right_down, double now)
  {
    if (stopped_) return ButtonEvent::None;
    valid = valid && std::isfinite(now) && (!initialized_ || now >= last_time_);
    if (!valid) {
      if (enabled_) return stop();
      released_seen_ = false;
      initialized_ = false;
      hold_since_.reset();
      return ButtonEvent::None;
    }
    last_time_ = now;
    if (!initialized_) {
      initialized_ = true;
      left_down_ = left_down;
      right_down_ = right_down;
    }
    // Starting with either button already down must never start motion.
    if (!released_seen_) {
      released_seen_ = !left_down && !right_down;
      remember(left_down, right_down);
      return ButtonEvent::None;
    }
    const bool right_pressed = right_down && !right_down_;
    const bool left_pressed = left_down && !left_down_;
    const bool left_released = !left_down && left_down_;
    remember(left_down, right_down);
    if (!enabled_) {
      if (right_pressed && !left_down) hold_since_ = now;
      if (!right_down || left_down) hold_since_.reset();
      if (hold_since_ && now - *hold_since_ >= 1.) {
        enabled_ = true;
        hold_since_.reset();
        return ButtonEvent::TransformUp;
      }
      return ButtonEvent::None;
    }
    // The startup hold is consumed. Its release is harmless; a NEW press stops
    // immediately and takes precedence over any simultaneous left-button event.
    if (right_pressed) return stop();
    if (left_pressed) return ButtonEvent::Rl;
    if (left_released) return ButtonEvent::ReturnToSit;
    return ButtonEvent::None;
  }

private:
  void remember(bool left, bool right) {left_down_ = left; right_down_ = right;}
  ButtonEvent stop() {stopped_ = true; return ButtonEvent::Stop;}
  bool initialized_{false}, released_seen_{false}, enabled_{false}, stopped_{false};
  bool left_down_{false}, right_down_{false};
  double last_time_{0.};
  std::optional<double> hold_since_;
};
}  // namespace tita
