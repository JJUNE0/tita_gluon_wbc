from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class PolicySpec:
    path: str
    input_obs_name: str
    input_history_name: str
    output_name: str
    obs_dim: int
    history_len: int
    action_dim: int


class PolicyRunner:
    """Strict ONNX runner for the exported NP3O TITA policy."""

    def __init__(self, spec: PolicySpec):
        try:
            import onnxruntime as ort
        except ImportError as exc:
            raise RuntimeError(
                "onnxruntime is required. Install it with: python3 -m pip install onnxruntime"
            ) from exc

        self.spec = spec
        self.session = ort.InferenceSession(spec.path, providers=["CPUExecutionProvider"])
        self._validate_interface()

    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "PolicyRunner":
        p = cfg["policy"]
        return cls(
            PolicySpec(
                path=p["path"],
                input_obs_name=p["input_obs_name"],
                input_history_name=p["input_history_name"],
                output_name=p["output_name"],
                obs_dim=int(p["obs_dim"]),
                history_len=int(p["history_len"]),
                action_dim=int(p["action_dim"]),
            )
        )

    def _validate_interface(self) -> None:
        inputs = {i.name: list(i.shape) for i in self.session.get_inputs()}
        outputs = {o.name: list(o.shape) for o in self.session.get_outputs()}
        expected_inputs = {self.spec.input_obs_name: [1, self.spec.obs_dim]}
        # history_len == 0: single-input policy (e.g. My16 -- no history buffer at all).
        # Don't require input_history_name to exist on the ONNX graph in that case.
        if self.spec.history_len > 0:
            expected_inputs[self.spec.input_history_name] = [1, self.spec.history_len, self.spec.obs_dim]
        expected_outputs = {self.spec.output_name: [1, self.spec.action_dim]}

        for name, shape in expected_inputs.items():
            if name not in inputs:
                raise ValueError(f"ONNX missing input {name!r}. Available inputs: {inputs}")
            if list(inputs[name]) != shape:
                raise ValueError(f"ONNX input {name!r} shape mismatch: {inputs[name]} != {shape}")

        for name, shape in expected_outputs.items():
            if name not in outputs:
                raise ValueError(f"ONNX missing output {name!r}. Available outputs: {outputs}")
            if list(outputs[name]) != shape:
                raise ValueError(f"ONNX output {name!r} shape mismatch: {outputs[name]} != {shape}")

    def act(self, obs_33: np.ndarray, history_10x33: np.ndarray | None = None) -> np.ndarray:
        obs = np.asarray(obs_33, dtype=np.float32).reshape(1, self.spec.obs_dim)
        feed = {self.spec.input_obs_name: obs}
        if self.spec.history_len > 0:
            hist = np.asarray(history_10x33, dtype=np.float32).reshape(
                1, self.spec.history_len, self.spec.obs_dim
            )
            feed[self.spec.input_history_name] = hist
        result = self.session.run([self.spec.output_name], feed)[0]
        return np.asarray(result, dtype=np.float32).reshape(self.spec.action_dim)
