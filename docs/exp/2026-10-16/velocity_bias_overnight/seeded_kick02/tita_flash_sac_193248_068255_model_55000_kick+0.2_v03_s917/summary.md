# tita_flash_sac_193248_068255_model_55000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "eed1eae0af8272ec7c19e71400ef380ad6fa44e0900331ce8eeae6bc37786919",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02138187935875732,
  "max_drift_m": 0.19611717889587588,
  "radial_IAE_m_s": 1.9131836367504063,
  "signed_longitudinal_delta_m": -0.02138107312557599,
  "tail_speed_mean_m_s": 0.00021239286331054298,
  "tail_speed_rms_m_s": 0.00021251795556939093,
  "tail_sensor_speed_mean_m_s": 0.00021241478870922422,
  "tail_fk_speed_mean_m_s": 0.00021084896571245333,
  "peak_tilt_rad": 0.16158077059476983,
  "peak_wheel_torque_nm": 1.6710946559906006,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.31191315915671103,
  "final_integral_m_s": 0.31191315915671103,
  "elapsed_wall_s": 11.263056501979008
}
```
