// ROBOT_COMMAND_FREE_RUNTIME: deterministic ONNX inference only; no ROS, SDK or CAN.
#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <onnxruntime_cxx_api.h>

int main(int argc, char ** argv)
{
  if (argc != 3) return 2;
  Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "posma2_check");
  Ort::SessionOptions options;
  options.SetIntraOpNumThreads(1);
  Ort::Session session(env, argv[1], options);
  if (session.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1] != 34 ||
    session.GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1] != 8)
  {
    throw std::runtime_error("incorrect actor dimensions");
  }
  Ort::AllocatorWithDefaultOptions allocator;
  auto in = session.GetInputNameAllocated(0, allocator);
  auto out = session.GetOutputNameAllocated(0, allocator);
  const char * inputs[] = {in.get()}, * outputs[] = {out.get()};
  auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  const std::array<int64_t, 2> shape{1, 34};
  std::array<float, 34> obs{};
  std::ifstream stream(argv[2]);
  if (!stream) throw std::runtime_error("missing fixture");
  std::cout.precision(10);
  while (stream >> obs[0]) {
    for (int i = 1; i < 34; ++i) {
      if (!(stream >> obs[i])) throw std::runtime_error("incomplete fixture");
    }
    auto tensor = Ort::Value::CreateTensor<float>(memory, obs.data(), obs.size(), shape.data(), 2);
    auto a = session.Run(Ort::RunOptions{nullptr}, inputs, &tensor, 1, outputs, 1);
    auto b = session.Run(Ort::RunOptions{nullptr}, inputs, &tensor, 1, outputs, 1);
    const auto * x = a[0].GetTensorData<float>();
    const auto * y = b[0].GetTensorData<float>();
    for (int i = 0; i < 8; ++i) {
      if (!std::isfinite(x[i]) || x[i] != y[i]) throw std::runtime_error("nonfinite/nondeterministic action");
      std::cout << x[i] << (i == 7 ? '\n' : ' ');
    }
  }
}
