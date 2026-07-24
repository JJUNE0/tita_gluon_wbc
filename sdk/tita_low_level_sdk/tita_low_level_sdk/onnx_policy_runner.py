from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np


@dataclass(frozen=True)
class PolicyStatus:
    loaded: bool
    detail: str
    input_names: tuple[str, ...]
    output_names: tuple[str, ...]


class OnnxPolicyRunner:
    """Fail-safe runner for My26 action-only or action+estimator diagnostic exports."""

    def __init__(self, policy_path: str, obs_dim: int = 33, history_len: int = 0, action_dim: int = 8) -> None:
        self.obs_dim = obs_dim
        self.history_len = history_len
        self.action_dim = action_dim
        self.session = None
        self.obs_input_name = ""
        self.history_input_name = ""
        self.output_name = ""
        self.estimator_output_name = ""
        self.last_estimator_scaled = np.zeros(3, dtype=np.float32)
        self.last_inference_ms = 0.0
        self.status = self._load(policy_path)

    def _load(self, policy_path: str) -> PolicyStatus:
        path = Path(policy_path).expanduser()
        if not path.is_file():
            return PolicyStatus(False, f"policy file not found: {path}", (), ())
        try:
            import onnxruntime as ort
        except ImportError:
            return PolicyStatus(False, "onnxruntime is not installed", (), ())
        try:
            self.session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
            inputs = self.session.get_inputs()
            outputs = self.session.get_outputs()
            if len(inputs) != 1 or len(outputs) not in (1, 2):
                raise ValueError("My26 policy must expose one input and one or two outputs")
            self.obs_input_name = self._find_input(inputs, 2, self.obs_dim, None)
            if self.obs_input_name != "nn_input0":
                raise ValueError(f"unexpected observation input name: {self.obs_input_name}")
            if self.history_len != 0:
                raise ValueError(f"My26 history_len must be 0, got {self.history_len}")
            self.output_name = self._find_output(outputs)
            if self.output_name != "nn_output":
                raise ValueError(f"unexpected policy output name: {self.output_name}")
            estimator_outputs = [
                item for item in outputs if len(list(item.shape)) == 2 and list(item.shape)[-1] == 3
            ]
            if len(outputs) == 2 and len(estimator_outputs) != 1:
                raise ValueError("diagnostic policy must expose exactly one [1,3] estimator output")
            if estimator_outputs:
                self.estimator_output_name = str(estimator_outputs[0].name)
            return PolicyStatus(
                True,
                f"loaded {path}",
                tuple(item.name for item in inputs),
                tuple(item.name for item in outputs),
            )
        except Exception as exc:  # ONNX Runtime reports several implementation-specific exceptions.
            self.session = None
            return PolicyStatus(False, f"ONNX load/interface validation failed: {exc}", (), ())

    def _find_input(self, inputs: list[object], rank: int, last_dim: int, middle_dim: int | None) -> str:
        for item in inputs:
            shape = list(item.shape)
            if len(shape) != rank or shape[-1] != last_dim:
                continue
            if middle_dim is not None and shape[-2] != middle_dim:
                continue
            return str(item.name)
        raise ValueError(f"missing ONNX input with rank={rank}, expected final dimensions {middle_dim}, {last_dim}")

    def _find_output(self, outputs: list[object]) -> str:
        for item in outputs:
            shape = list(item.shape)
            if len(shape) == 2 and shape[-1] == self.action_dim:
                return str(item.name)
        raise ValueError(f"missing ONNX output with final dimension {self.action_dim}")

    def act(self, obs_current: np.ndarray, obs_history: np.ndarray | None = None) -> np.ndarray:
        if self.session is None:
            raise RuntimeError(self.status.detail)
        obs = np.asarray(obs_current, dtype=np.float32).reshape(1, self.obs_dim)
        if obs_history is not None and np.asarray(obs_history).size != 0:
            raise ValueError("My26 policy has no history input")
        started = perf_counter()
        output = self.session.run([self.output_name], {self.obs_input_name: obs})[0]
        self.last_inference_ms = (perf_counter() - started) * 1000.0
        action = np.asarray(output, dtype=np.float32).reshape(self.action_dim)
        if not np.all(np.isfinite(action)):
            raise ValueError("ONNX action contains NaN or Inf")
        return action

    def act_with_estimator(self, obs_current: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if self.session is None:
            raise RuntimeError(self.status.detail)
        if not self.estimator_output_name:
            raise RuntimeError("policy does not expose an estimator output")
        obs = np.asarray(obs_current, dtype=np.float32).reshape(1, self.obs_dim)
        started = perf_counter()
        action_output, estimator_output = self.session.run(
            [self.output_name, self.estimator_output_name], {self.obs_input_name: obs}
        )
        self.last_inference_ms = (perf_counter() - started) * 1000.0
        action = np.asarray(action_output, dtype=np.float32).reshape(self.action_dim)
        estimator = np.asarray(estimator_output, dtype=np.float32).reshape(3)
        if not np.all(np.isfinite(action)) or not np.all(np.isfinite(estimator)):
            raise ValueError("ONNX action or estimator contains NaN or Inf")
        self.last_estimator_scaled = estimator.copy()
        return action, estimator
