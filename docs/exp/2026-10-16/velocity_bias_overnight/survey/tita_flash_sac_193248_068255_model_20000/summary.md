# tita_flash_sac_193248_068255_model_20000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "11a4a73216c0aa0c4a6cf7ec34a051ca441011e4453039e07852bb5ce051f86d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.043559434075476,
  "max_drift_m": 13.043559434075476,
  "radial_IAE_m_s": 391.9435262717909,
  "signed_longitudinal_delta_m": 12.92619240976366,
  "tail_speed_mean_m_s": 0.21848595134416848,
  "tail_speed_rms_m_s": 0.21848595135879106,
  "tail_sensor_speed_mean_m_s": 0.2180144180191515,
  "tail_fk_speed_mean_m_s": 0.21800454559403,
  "peak_tilt_rad": 0.15956155825553608,
  "peak_wheel_torque_nm": 0.2667994499206543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.4159237400162965
}
```
