# tita_flash_sac_193248_068255_model_45000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "e66d68dbbcd457edbae379880ac87a33964efebb9a21af14c3465d1b4669dd07",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.814400620868517,
  "max_drift_m": 9.814400620868517,
  "radial_IAE_m_s": 293.74352295256864,
  "signed_longitudinal_delta_m": -9.739221289144218,
  "tail_speed_mean_m_s": -0.16539534017664256,
  "tail_speed_rms_m_s": 0.1653959074218834,
  "tail_sensor_speed_mean_m_s": -0.16515245487089744,
  "tail_fk_speed_mean_m_s": -0.1651659001908393,
  "peak_tilt_rad": 0.020217226062084315,
  "peak_wheel_torque_nm": 0.07495564222335815,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.514032676001079
}
```
