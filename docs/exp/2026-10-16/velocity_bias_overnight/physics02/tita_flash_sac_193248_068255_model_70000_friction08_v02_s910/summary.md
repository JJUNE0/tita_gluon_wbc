# tita_flash_sac_193248_068255_model_70000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "7d106d78d3f67b7819e0b6e231f3f0551c3da8554afc2f7cd674d5f38c403962",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007296869889153538,
  "max_drift_m": 0.007917107361380817,
  "radial_IAE_m_s": 0.37802722921651616,
  "signed_longitudinal_delta_m": 0.007296682480579597,
  "tail_speed_mean_m_s": 3.2797548878078735e-05,
  "tail_speed_rms_m_s": 3.27985507631574e-05,
  "tail_sensor_speed_mean_m_s": 3.284794141648563e-05,
  "tail_fk_speed_mean_m_s": 3.2655095070572364e-05,
  "peak_tilt_rad": 0.0736333966571705,
  "peak_wheel_torque_nm": 0.06934140622615814,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.07411114320043787,
  "final_integral_m_s": 0.07404670130360866,
  "elapsed_wall_s": 15.65383116400335
}
```
