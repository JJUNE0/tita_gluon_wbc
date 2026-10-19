# tita_flash_sac_193248_068255_model_70000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "f00706cd651def7f9f8f616fe3d93c931ce34a3bbbbf7fa9887c24d440efbfa8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011997711642695611,
  "max_drift_m": 0.012438446933632994,
  "radial_IAE_m_s": 0.5712777832736609,
  "signed_longitudinal_delta_m": 0.011997611808279202,
  "tail_speed_mean_m_s": 8.223452613427304e-05,
  "tail_speed_rms_m_s": 8.223707624140236e-05,
  "tail_sensor_speed_mean_m_s": 8.217818956372241e-05,
  "tail_fk_speed_mean_m_s": 8.198592198848994e-05,
  "peak_tilt_rad": 0.07355984343411848,
  "peak_wheel_torque_nm": 0.06639309972524643,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.07339869487107538,
  "final_integral_m_s": 0.07339869487107538,
  "elapsed_wall_s": 8.67486262798775
}
```
