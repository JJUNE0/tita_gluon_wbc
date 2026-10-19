# tita_flash_sac_115632_883848_model_10000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "88d474b997cd07f6300235f1a52e3ec15114d895655cf5404bcb21bbd6a4ba5b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.032470253056838955,
  "max_drift_m": 0.039990340951486486,
  "radial_IAE_m_s": 2.0062836202681154,
  "signed_longitudinal_delta_m": 0.032439324911943436,
  "tail_speed_mean_m_s": -0.00010722724601797897,
  "tail_speed_rms_m_s": 0.0163812579505559,
  "tail_sensor_speed_mean_m_s": -0.0016334377057489625,
  "tail_fk_speed_mean_m_s": -0.00015329604226990866,
  "peak_tilt_rad": 0.11337907331768249,
  "peak_wheel_torque_nm": 2.9462568759918213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29410720764922976,
  "final_integral_m_s": 0.2858184355667128,
  "elapsed_wall_s": 17.526074117980897
}
```
