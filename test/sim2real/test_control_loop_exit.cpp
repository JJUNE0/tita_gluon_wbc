// DESKTOP_DRY_RUN: real shutdown helper, mock writer only; no ROS/SDK/CAN.
#include <array>
#include <atomic>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>
#include "tita_controller/control_loop_exit.hpp"
using namespace tita;
using Torque = std::array<double, 8>;
void check(bool ok, const char * text) {if (!ok) throw std::runtime_error(text);}
int main()
{
  int cases = 0;
  {
    bool enabled = true; std::vector<Torque> sent; int waits = 0;
    auto result = run_with_torque_release([&] {sent.push_back(Torque{1.,2.,3.,4.,5.,6.,7.,8.});}, enabled,
      [&] {sent.push_back(Torque{}); return true;}, [&] {++waits;});
    check(sent.size()==11 && sent.front()[0]==1., "work executes before cleanup");
    for (std::size_t i=1; i<sent.size(); ++i) check(sent[i]==Torque{}, "all final frames zero");
    check(!enabled && !result.loop_error && !result.zero_failed && result.accepted==10 && waits==9,
      "bounded normal release and output latch"); ++cases;
  }
  {
    bool enabled = false; int sends = 0;
    const auto result = run_with_torque_release([] {}, enabled, [&] {++sends; return true;}, [] {});
    check(sends==0 && !result.zero_requested && !enabled, "disabled output remains command free"); ++cases;
  }
  {
    bool enabled = true; int sends = 0;
    const auto result = run_with_torque_release([] {throw std::runtime_error("ROS context invalid");},
      enabled, [&] {++sends; return true;}, [] {});
    check(result.loop_error && sends==10 && !enabled, "loop exception still releases");
    try {std::rethrow_exception(result.loop_error);} catch (const std::runtime_error & e) {
      check(std::string(e.what())=="ROS context invalid", "exception preserved");
    } ++cases;
  }
  for (bool throws : {false,true}) {
    bool enabled = true; int calls = 0;
    const auto result = run_with_torque_release([] {}, enabled, [&] {
      if (++calls==3) {if (throws) throw std::runtime_error("CAN failure"); return false;}
      return true;
    }, [] {});
    check(result.zero_failed && result.attempts==3 && result.accepted==2 && calls==3 && !enabled,
      "first failed/throwing transport stops further sends"); ++cases;
  }
  {
    bool enabled = true; int calls=0;
    const auto result = run_with_torque_release([&] {enabled=false;}, enabled,
      [&] {++calls; return true;}, [] {});
    check(calls==0 && !result.zero_requested, "prior CAN failure latch is not retried"); ++cases;
  }
  {
    bool enabled=true;
    const auto result=run_with_torque_release([] {},enabled,[] {return true;},
      [] {throw std::runtime_error("sleep failed");});
    check(result.zero_failed && result.accepted==1 && result.attempts==1 && !enabled,
      "cleanup wait failure is contained"); ++cases;
  }
  {
    bool enabled=true; int calls=0;
    const auto result=run_with_torque_release([] {throw 42;},enabled,
      [&] {++calls;return true;},[] {});
    check(result.loop_error && calls==10 && !enabled, "non-std loop exceptions are contained"); ++cases;
  }
  {
    std::atomic_bool running{true},entered{false}; bool enabled=true;
    std::vector<int> events;
    std::thread worker([&] {
      run_with_torque_release([&] {
        events.push_back(1); entered=true;
        while (running) std::this_thread::yield();
        events.push_back(2);  // Last in-flight nonzero motor command before loop exit.
      },enabled,[&] {events.push_back(0);return true;},[] {});
    });
    while (!entered) std::this_thread::yield();
    running=false; worker.join(); events.push_back(3);  // SDK destruction only after join.
    check(events.size()==13 && events[0]==1 && events[1]==2 && events.back()==3,
      "writer joined before SDK teardown");
    for (std::size_t i=2;i<12;++i) check(events[i]==0,"zero commands follow last in-flight command");
    check(!enabled,"worker closes output before SDK teardown"); ++cases;
  }
  std::cout << "PASS DESKTOP_DRY_RUN: " << cases
            << " shutdown scenarios, zero ordering/bounds, disabled gate, exceptions, transport failure, sole-writer join\n";
}
