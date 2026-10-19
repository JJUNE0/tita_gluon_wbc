# tita_flash_sac_115632_883848_model_30000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "f3e743119e5b041a15b54a45ac6094d290a65283ae3f05f4cc4f6cbd7ee7eccd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002010613925736193,
  "max_drift_m": 0.009437038549634985,
  "radial_IAE_m_s": 0.0656917999833863,
  "signed_longitudinal_delta_m": -0.002008274010364472,
  "tail_speed_mean_m_s": -3.209666977239574e-05,
  "tail_speed_rms_m_s": 3.223266351956532e-05,
  "tail_sensor_speed_mean_m_s": -3.233873379202658e-05,
  "tail_fk_speed_mean_m_s": -3.193869462422589e-05,
  "peak_tilt_rad": 0.08649522342477711,
  "peak_wheel_torque_nm": 0.3397175669670105,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.015505603341892547,
  "final_integral_m_s": -0.015448516695906005,
  "elapsed_wall_s": 12.774328614003025
}
```
