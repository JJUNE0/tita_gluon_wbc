// DESKTOP_DRY_RUN: teacher target reconstruction without robot/CAN construction.
#include <cassert>
#include <cmath>
#include <iostream>
#include <limits>
#include <random>
#include "tita_controller/adapter.hpp"

int main()
{
  const std::array<int, 8> mapping{7, 0, 3, 4, 2, 1, 6, 5};
  std::vector<tita::ActionTerm> terms;
  for (int joint : mapping) {
    terms.push_back({joint, joint == 3 || joint == 7,
      joint == 7 ? -20. : joint == 3 ? 5. : .25, .1, -100., 100.});
  }
  tita::Joints kp{}, kd{}, limits{}, q{}, dq{};
  kp.fill(10.); kd.fill(.5); limits.fill(12.);
  tita::ActionAdapter adapter(terms, kp, kd, limits);
  std::mt19937 rng(20261017);
  std::uniform_real_distribution<double> random(-1., 1.);
  for (int trial = 0; trial < 2000; ++trial) {
    std::vector<float> raw(8);
    for (std::size_t i = 0; i < 8; ++i) {
      raw[i] = static_cast<float>(random(rng));
      q[i] = random(rng); dq[i] = 20. * random(rng);
    }
    const auto original = raw;
    const std::array<double, 2> bias{2. * random(rng), 2. * random(rng)};
    tita::Joints teacher{};
    assert(adapter.teacher_action(raw, bias, teacher));
    std::vector<float> student(teacher.begin(), teacher.end());
    const auto actual = adapter.compute(raw, q, dq, bias);
    const auto reproduced = adapter.compute(student, q, dq);
    for (std::size_t i = 0; i < 8; ++i) {
      const auto & t = terms[i];
      const double target = raw[i] * t.scale + t.offset +
        (t.velocity ? bias[t.joint / 4] : 0.);
      assert(std::abs(teacher[i] * t.scale + t.offset - target) < 1e-12);
      assert(std::abs(actual[i] - reproduced[i]) < 2e-5);
    }
    assert(raw == original);
  }
  // Raw target clipping must happen before wheel bias; post-clip unreachable
  // targets remain logged but are marked invalid instead of silently clipped.
  std::vector<float> raw(8, 0.f);
  raw[0] = -10.f;  // right wheel: clipped physical target +100 rad/s.
  tita::Joints teacher{};
  assert(!adapter.teacher_action(raw, {0., 1.}, teacher));
  assert(std::abs(teacher[0] * terms[0].scale + .1 - 101.) < 1e-12);
  assert(adapter.teacher_action(raw, {0., -1.}, teacher));
  assert(std::abs(teacher[0] * terms[0].scale + .1 - 99.) < 1e-12);
  raw[0] = std::numeric_limits<float>::quiet_NaN();
  assert(!adapter.teacher_action(raw, {}, teacher));
  assert(!adapter.teacher_action({}, {}, teacher));
  terms[0].scale = 0.;
  tita::ActionAdapter zero_scale(terms, kp, kd, limits);
  assert(!zero_scale.teacher_action(std::vector<float>(8, 0.f), {}, teacher));
  std::cout << "PASS: 2000 teacher/PD round trips; reordered joints, negative/unequal scales, "
    "offsets, saturation, post-clip bias, invalid inputs; raw actions unchanged\n";
}
