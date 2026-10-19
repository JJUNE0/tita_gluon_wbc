# tita_flash_sac_193248_068255_model_70000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "8a58e584ff1e22a4410ccef751117297747e00ce478c601193a0c9ce3a6b7cf2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020002832928800864,
  "max_drift_m": 0.025777783416480626,
  "radial_IAE_m_s": 1.046482555508561,
  "signed_longitudinal_delta_m": 0.020002766097631075,
  "tail_speed_mean_m_s": 7.920495557450835e-05,
  "tail_speed_rms_m_s": 7.92123429504875e-05,
  "tail_sensor_speed_mean_m_s": 7.915848654049202e-05,
  "tail_fk_speed_mean_m_s": 7.890639772451996e-05,
  "peak_tilt_rad": 0.07899228149481519,
  "peak_wheel_torque_nm": 0.21579483151435852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.012639915047393781,
  "final_integral_m_s": 0.012639915047393781,
  "elapsed_wall_s": 7.967492914991453
}
```
