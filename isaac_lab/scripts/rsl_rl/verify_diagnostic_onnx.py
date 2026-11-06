"""Verify that a diagnostic ONNX preserves the original action output."""

from __future__ import annotations

import argparse
import json

import numpy as np
import onnxruntime as ort


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--samples", required=True)
    args = parser.parse_args()

    obs = np.asarray(np.load(args.samples)["nn_input0"], dtype=np.float32)
    original = ort.InferenceSession(args.original, providers=["CPUExecutionProvider"])
    diagnostic = ort.InferenceSession(args.diagnostic, providers=["CPUExecutionProvider"])
    original_actions = []
    diagnostic_actions = []
    estimators = []
    for sample in obs:
        inputs = {"nn_input0": sample.reshape(1, 33)}
        original_actions.append(original.run(["nn_output"], inputs)[0].reshape(8))
        outputs = diagnostic.run(None, inputs)
        diagnostic_actions.append(outputs[0].reshape(8))
        estimators.append(outputs[1].reshape(3))
    difference = np.abs(
        np.asarray(original_actions) - np.asarray(diagnostic_actions)
    )
    estimator = np.asarray(estimators)
    report = {
        "sample_count": int(obs.shape[0]),
        "action_max_abs_diff": float(difference.max()),
        "action_mean_abs_diff": float(difference.mean()),
        "estimator_shape": list(estimator.shape),
        "finite": bool(np.isfinite(estimator).all()),
        "diagnostic_outputs": [
            [output.name, list(output.shape), output.type]
            for output in diagnostic.get_outputs()
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["action_max_abs_diff"] != 0.0 or not report["finite"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
