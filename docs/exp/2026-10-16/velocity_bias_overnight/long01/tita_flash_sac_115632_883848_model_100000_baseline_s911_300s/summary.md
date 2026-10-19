# tita_flash_sac_115632_883848_model_100000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "9ec93955f69bc8abe6eb5e69a3da6be609f67f2389d66d00f16b1e686f70290e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 33.21916598375844,
  "max_drift_m": 33.21916598375844,
  "radial_IAE_m_s": 5043.818302448481,
  "signed_longitudinal_delta_m": 32.720470244419204,
  "tail_speed_mean_m_s": 0.11025855789878006,
  "tail_speed_rms_m_s": 0.11025855792144346,
  "tail_sensor_speed_mean_m_s": 0.11001974879903398,
  "tail_fk_speed_mean_m_s": 0.11001923779527557,
  "peak_tilt_rad": 0.08952284931837506,
  "peak_wheel_torque_nm": 0.39562851190567017,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 53.07745291502215
}
```
