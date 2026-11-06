"""Expose an embedded estimator tensor as a diagnostic ONNX output.

This does not alter the action graph. It only appends the existing estimator
tensor to the graph outputs so deployment logging can record it.
"""

from __future__ import annotations

import argparse

import onnx
from onnx import TensorProto, helper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--tensor",
        default="/estimator/estimator.4/Gemm_output_0",
    )
    args = parser.parse_args()

    model = onnx.load(args.input)
    available = {name for node in model.graph.node for name in node.output}
    if args.tensor not in available:
        raise ValueError(f"estimator tensor not found: {args.tensor}")
    if any(output.name == args.tensor for output in model.graph.output):
        raise ValueError(f"tensor is already a graph output: {args.tensor}")

    model.graph.output.append(
        helper.make_tensor_value_info(args.tensor, TensorProto.FLOAT, [1, 3])
    )
    onnx.checker.check_model(model)
    onnx.save(model, args.output)


if __name__ == "__main__":
    main()
