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
    """Fail-safe ONNX runner for the fixed [1,33], [1,10,33] TITA policy interface."""

    def __init__(self, policy_path: str, obs_dim: int = 33, history_len: int = 10, action_dim: int = 8) -> None:
        self.obs_dim = obs_dim
        self.history_len = history_len
        self.action_dim = action_dim
        self.session = None
        self.obs_input_name = ""
        self.history_input_name = ""
        self.output_name = ""
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
            self.obs_input_name = self._find_input(inputs, 2, self.obs_dim, None)
            self.history_input_name = self._find_input(inputs, 3, self.obs_dim, self.history_len)
            self.output_name = self._find_output(outputs)
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

    def act(self, obs_current: np.ndarray, obs_history: np.ndarray) -> np.ndarray:
        if self.session is None:
            raise RuntimeError(self.status.detail)
        obs = np.asarray(obs_current, dtype=np.float32).reshape(1, self.obs_dim)
        history = np.asarray(obs_history, dtype=np.float32).reshape(1, self.history_len, self.obs_dim)
        started = perf_counter()
        output = self.session.run(
            [self.output_name], {self.obs_input_name: obs, self.history_input_name: history}
        )[0]
        self.last_inference_ms = (perf_counter() - started) * 1000.0
        action = np.asarray(output, dtype=np.float32).reshape(self.action_dim)
        if not np.all(np.isfinite(action)):
            raise ValueError("ONNX action contains NaN or Inf")
        return action
