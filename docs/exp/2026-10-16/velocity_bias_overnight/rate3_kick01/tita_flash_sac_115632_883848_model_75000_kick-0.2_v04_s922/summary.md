# tita_flash_sac_115632_883848_model_75000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "c6c9b3d4cea365fa328498c811e553172cc0fca051bf471d31299ca09569c6b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03735360849172698,
  "max_drift_m": 0.12404825699540688,
  "radial_IAE_m_s": 2.342444326230436,
  "signed_longitudinal_delta_m": 0.03735298499885781,
  "tail_speed_mean_m_s": 3.0646480919841484e-05,
  "tail_speed_rms_m_s": 3.181830810167483e-05,
  "tail_sensor_speed_mean_m_s": 3.0663251385795245e-05,
  "tail_fk_speed_mean_m_s": 3.130089698126441e-05,
  "peak_tilt_rad": 0.11027368608974641,
  "peak_wheel_torque_nm": 1.5855762958526611,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.005727509596362988,
  "final_integral_m_s": 0.005727509596362988,
  "elapsed_wall_s": 8.838015248999
}
```
