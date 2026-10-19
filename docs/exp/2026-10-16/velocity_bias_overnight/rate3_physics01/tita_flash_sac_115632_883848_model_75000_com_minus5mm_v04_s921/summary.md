# tita_flash_sac_115632_883848_model_75000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "db3ea6a6735372b2e1d718ed884f619bb7445e728475176ef8315b1bbb4fb604",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03976988020782033,
  "max_drift_m": 0.05422072144837519,
  "radial_IAE_m_s": 2.282875792590242,
  "signed_longitudinal_delta_m": 0.03976597198412763,
  "tail_speed_mean_m_s": 5.932475263064691e-05,
  "tail_speed_rms_m_s": 6.0008976392762654e-05,
  "tail_sensor_speed_mean_m_s": 5.917845889773504e-05,
  "tail_fk_speed_mean_m_s": 5.9771752614612e-05,
  "peak_tilt_rad": 0.07577220635772486,
  "peak_wheel_torque_nm": 0.48651933670043945,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.06522912373009268,
  "final_integral_m_s": -0.06522912373009268,
  "elapsed_wall_s": 6.195411494001746
}
```
