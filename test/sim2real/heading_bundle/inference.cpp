// ROBOT_COMMAND_FREE_RUNTIME: deterministic ONNX inference only (observation size from the model); no ROS, SDK or CAN.
#include <cmath>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <onnxruntime_cxx_api.h>

int main(int argc, char ** argv)
{
  if (argc != 3) return 2;
  Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "heading_check");
  Ort::SessionOptions options;
  options.SetIntraOpNumThreads(1);
  Ort::Session session(env, argv[1], options);
  const auto n = session.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1];
  if (n != 35 || session.GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()[1] != 8) {
    throw std::runtime_error("incorrect actor dimensions");
  }
  Ort::AllocatorWithDefaultOptions allocator;
  auto in = session.GetInputNameAllocated(0, allocator);
  auto out = session.GetOutputNameAllocated(0, allocator);
  const char * inputs[] = {in.get()}, * outputs[] = {out.get()};
  auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  const std::vector<int64_t> shape{1, n};
  std::vector<float> obs(static_cast<std::size_t>(n));
  std::ifstream stream(argv[2]);
  if (!stream) throw std::runtime_error("missing fixture");
  std::cout.precision(10);
  while (stream >> obs[0]) {
    for (std::size_t i = 1; i < obs.size(); ++i) {
      if (!(stream >> obs[i])) throw std::runtime_error("incomplete fixture");
    }
    auto tensor = Ort::Value::CreateTensor<float>(memory, obs.data(), obs.size(), shape.data(), 2);
    auto a = session.Run(Ort::RunOptions{nullptr}, inputs, &tensor, 1, outputs, 1);
    auto b = session.Run(Ort::RunOptions{nullptr}, inputs, &tensor, 1, outputs, 1);
    const auto * x = a[0].GetTensorData<float>();
    const auto * y = b[0].GetTensorData<float>();
    for (int i = 0; i < 8; ++i) {
      if (x[i] != y[i] || !std::isfinite(x[i])) throw std::runtime_error("non-deterministic or non-finite output");
      std::cout << x[i] << (i == 7 ? '\n' : ' ');
    }
  }
}
