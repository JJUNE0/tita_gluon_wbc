// DESKTOP_DRY_RUN / ARM command-free: production filter + adapter, no ROS/SDK/CAN.
#include <iostream>
#include <limits>
#include "tita_controller/leg_action_filter.hpp"
#include "tita_controller/adapter.hpp"
using namespace tita;
void check(bool value) {if (!value) throw std::runtime_error("filter assertion failed");}
int main(int argc, char **)
{
  if (argc > 1) {
    std::string mode; std::cin >> mode;
    std::vector<int64_t> order(8);
    for (auto & j : order) std::cin >> j;
    double hz=8.3,q=3.;
    if (mode=="ma2_notch_legs") std::cin >> hz >> q;
    LegActionFilter filter(mode, order,hz,q);
    int reset;
    std::cout.precision(17);
    while (std::cin >> reset) {
      if (reset) filter.reset();
      std::vector<float> raw(8);
      for (auto & a : raw) std::cin >> a;
      for (float a : filter.update(raw)) std::cout << a << ' ';
      std::cout << '\n';
    }
    return 0;
  }
  const std::vector<int64_t> order{0,1,2,3,4,5,6,7};
  LegActionFilter f("ma2_legs", order), off("none", order);
  std::vector<float> a{1,2,3,4,5,6,7,8}, b{-1,-2,-3,-4,-5,-6,-7,-8};
  check(f.update(a)==a);  // First action has no synthetic zero history.
  const auto applied=f.update(b);
  check(applied==std::vector<float>({0,0,0,-4,0,0,0,-8}));
  check(a==std::vector<float>({1,2,3,4,5,6,7,8}));
  check(off.update(a)==a && off.update(b)==b);
  for (int i=0;i<100;++i) {
    const auto out=f.update(i%2==0?a:b);
    for (int j : {0,1,2,4,5,6}) check(out[j]==0.f);
  }
  f.reset(); check(f.update(b)==b); check(f.update(b)==b);
  bool rejected=false;
  auto bad=a; bad[0]=std::numeric_limits<float>::quiet_NaN();
  try {f.update(bad);} catch (const std::exception &) {rejected=true;}
  check(rejected);
  rejected=false;
  try {LegActionFilter invalid("ma2_all",order);} catch (const std::exception &) {rejected=true;}
  check(rejected);
  rejected=false;
  try {LegActionFilter invalid("none",{0,1,2,3,4,5,6,6});} catch (const std::exception &) {rejected=true;}
  check(rejected);
  LegActionFilter mapped("ma2_legs",{3,0,7,1,2,4,5,6});
  mapped.update(a); const auto p=mapped.update(b);
  check(p[0]==b[0] && p[2]==b[2] && p[3]==0.f);
  std::vector<ActionTerm> terms;
  for (int j=0;j<8;++j) terms.push_back({j,j==3||j==7,.25,0.,-1.,1.});
  Joints kp{60,60,92,0,60,60,92,0},kd{1.5,1.5,2.3,.5,1.5,1.5,2.3,.5};
  ActionAdapter adapter(terms,kp,kd,{60,60,60,12,60,60,60,12});
  Joints teacher{}; const std::array<double,2> bias{.1,.1};
  check(adapter.teacher_action(applied,bias,teacher));
  const auto actual=adapter.compute(applied,Joints{},Joints{},bias);
  const auto rebuilt=adapter.compute(std::vector<float>(teacher.begin(),teacher.end()),Joints{},Joints{});
  for (int j=0;j<8;++j) check(std::abs(actual[j]-rebuilt[j])<1e-6);
  check(teacher[0]==applied[0] && teacher[0]!=b[0]);
  LegActionFilter notch("ma2_notch_legs",order);
  check(notch.update(a)==a);
  for (int i=0;i<100;++i) check(notch.update(a)==a);
  notch.reset();check(notch.update(b)==b);
  notch.reset();
  for (int i=0;i<2000;++i) {
    const float value=std::sin(2.*std::acos(-1.)*8.3*i/50.)+.3*(i%2==0?1.:-1.);
    const auto output=notch.update(std::vector<float>(8,value));
    check(output[3]==value && output[7]==value);
    if (i>1000) for (int j : {0,1,2,4,5,6}) check(std::abs(output[j])<1e-6);
  }
  rejected=false;
  try {LegActionFilter invalid("ma2_notch_legs",order,24.,.5);} catch (const std::exception &) {rejected=true;}
  check(rejected);
  std::cout << "PASS: first action/DC, period-2, wheels, reset, raw preservation, OFF parity, "
               "mapping, invalid input/mode, notch 8.3 Hz/DC/reset, teacher plus bias torque reconstruction\n";
}
