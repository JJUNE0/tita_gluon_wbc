# tita_flash_sac_193248_068255_model_45000_com+0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com+0.005_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "1156c32bb1a04878f247ea453fee08bfd897abc99d3ad136725ce7e74e7321b9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.340125848470623,
  "max_drift_m": 6.340125848470623,
  "radial_IAE_m_s": 186.86099855886988,
  "signed_longitudinal_delta_m": -6.315944250666642,
  "tail_speed_mean_m_s": -0.1100413520163846,
  "tail_speed_rms_m_s": 0.11005230916944683,
  "tail_sensor_speed_mean_m_s": -0.10988637450914052,
  "tail_fk_speed_mean_m_s": -0.10989709088700685,
  "peak_tilt_rad": 0.03440234819791099,
  "peak_wheel_torque_nm": 0.08740812540054321,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.500802538008429
}
```
