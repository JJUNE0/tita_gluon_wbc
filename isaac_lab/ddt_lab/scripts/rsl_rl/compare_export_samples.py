"""ONNX Runtime half of ``validate_export_parity.py``.

Kept separate because the Isaac Lab Python 3.11 environment and the ROS/Jazzy
ONNX Runtime Python 3.12 environment intentionally differ on this machine.
"""

import argparse
import hashlib
import json
import os
import time

import numpy as np
import onnxruntime as ort

parser = argparse.ArgumentParser()
parser.add_argument("--samples", required=True)
parser.add_argument("--checkpoint", required=True)
parser.add_argument("--onnx", required=True)
parser.add_argument("--task", required=True)
parser.add_argument("--out_dir", required=True)
args = parser.parse_args()


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


data = np.load(args.samples)
captured_obs = np.asarray(data["nn_input0"], dtype=np.float32)
native_outputs = np.asarray(data["pytorch_output"], dtype=np.float32)
session = ort.InferenceSession(args.onnx, providers=["CPUExecutionProvider"])
input_meta = [(item.name, list(item.shape), item.type) for item in session.get_inputs()]
output_meta = [(item.name, list(item.shape), item.type) for item in session.get_outputs()]
expected_inputs = [("nn_input0", [1, 33], "tensor(float)")]
expected_outputs = [("nn_output", [1, 8], "tensor(float)")]
if input_meta != expected_inputs or output_meta != expected_outputs:
    raise ValueError(f"unexpected ONNX interface: inputs={input_meta}, outputs={output_meta}")

onnx_outputs = []
inference_ms = []
for sample in captured_obs:
    start_ns = time.perf_counter_ns()
    output = session.run(["nn_output"], {"nn_input0": sample.reshape(1, 33)})[0]
    inference_ms.append((time.perf_counter_ns() - start_ns) / 1.0e6)
    onnx_outputs.append(output.reshape(8))
onnx_outputs = np.asarray(onnx_outputs, dtype=np.float32)
abs_diff = np.abs(native_outputs - onnx_outputs)
if not np.isfinite(onnx_outputs).all():
    raise ValueError("non-finite ONNX output")

samples_path = os.path.join(args.out_dir, "parity_samples.npz")
report_path = os.path.join(args.out_dir, "parity_report.json")
np.savez_compressed(
    samples_path,
    nn_input0=captured_obs,
    pytorch_output=native_outputs,
    onnx_output=onnx_outputs,
    abs_diff=abs_diff,
)
report = {
    "environment": "TRAINING_SIM",
    "task": args.task,
    "checkpoint_path": os.path.abspath(args.checkpoint),
    "checkpoint_sha256": sha256(args.checkpoint),
    "onnx_path": os.path.abspath(args.onnx),
    "onnx_sha256": sha256(args.onnx),
    "input_interface": input_meta,
    "output_interface": output_meta,
    "sample_source": "Isaac Lab rollout, native policy inputs before each env step",
    "sample_count": int(captured_obs.shape[0]),
    "input_shape": list(captured_obs.shape),
    "output_shape": list(native_outputs.shape),
    "dtype": str(native_outputs.dtype),
    "runtime_provider": session.get_providers(),
    "max_abs_diff": float(abs_diff.max()),
    "mean_abs_diff": float(abs_diff.mean()),
    "inference_ms_mean": float(np.mean(inference_ms)),
    "inference_ms_max": float(np.max(inference_ms)),
    "finite": True,
    "samples_artifact": os.path.abspath(samples_path),
}
with open(report_path, "w", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)
    stream.write("\n")
print(json.dumps(report, indent=2, sort_keys=True))
