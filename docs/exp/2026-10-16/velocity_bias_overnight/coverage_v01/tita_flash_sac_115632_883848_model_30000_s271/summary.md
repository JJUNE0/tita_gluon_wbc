# tita_flash_sac_115632_883848_model_30000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "03f0d167fb161ab76c394797e7a9fc1890dfe31eb3baca0b038b0be4d1b25f2a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.050751496152877815,
  "max_drift_m": 0.12516898437486385,
  "radial_IAE_m_s": 3.179615367727847,
  "signed_longitudinal_delta_m": 0.05074058154298315,
  "tail_speed_mean_m_s": -6.102315680246217e-05,
  "tail_speed_rms_m_s": 6.105071137029029e-05,
  "tail_sensor_speed_mean_m_s": -6.189862214728434e-05,
  "tail_fk_speed_mean_m_s": -6.0537673143725066e-05,
  "peak_tilt_rad": 0.11731439769486829,
  "peak_wheel_torque_nm": 1.1866579055786133,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5397877633856539,
  "final_integral_m_s": 0.5399024936315568,
  "elapsed_wall_s": 4.285910631006118
}
```
