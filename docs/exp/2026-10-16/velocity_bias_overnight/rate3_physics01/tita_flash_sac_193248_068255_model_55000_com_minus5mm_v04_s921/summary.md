# tita_flash_sac_193248_068255_model_55000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "6fb3d1ce7d9925099a3b1baca37584047fdf68e0990ef04706d5121a993fd38d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015385268377270998,
  "max_drift_m": 0.05660997459096676,
  "radial_IAE_m_s": 1.2991263872284797,
  "signed_longitudinal_delta_m": -0.015376149274030668,
  "tail_speed_mean_m_s": 0.0001916559638181948,
  "tail_speed_rms_m_s": 0.00019179418762446494,
  "tail_sensor_speed_mean_m_s": 0.0001918481496589202,
  "tail_fk_speed_mean_m_s": 0.0001900499829372876,
  "peak_tilt_rad": 0.1289664058270552,
  "peak_wheel_torque_nm": 0.7415735125541687,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23151766742544794,
  "final_integral_m_s": 0.23151766742544794,
  "elapsed_wall_s": 7.064802000997588
}
```
