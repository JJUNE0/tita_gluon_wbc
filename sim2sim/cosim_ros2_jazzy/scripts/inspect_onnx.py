#!/usr/bin/env python3
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("policy")
    args = parser.parse_args()

    import onnxruntime as ort

    session = ort.InferenceSession(args.policy, providers=["CPUExecutionProvider"])
    print("== Inputs ==")
    for i in session.get_inputs():
        print(i.name, list(i.shape), i.type)
    print("== Outputs ==")
    for o in session.get_outputs():
        print(o.name, list(o.shape), o.type)


if __name__ == "__main__":
    main()
