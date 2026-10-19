# tita_flash_sac_115632_883848_model_75000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "4b02bf0364b7e0988f8b93878e08e4c0508784fe4bd336e9ef4b657831bf837d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022937645098900963,
  "max_drift_m": 0.06234564797299901,
  "radial_IAE_m_s": 1.3933160584419548,
  "signed_longitudinal_delta_m": 0.02293764496052301,
  "tail_speed_mean_m_s": 3.07965694307371e-05,
  "tail_speed_rms_m_s": 3.085026539493552e-05,
  "tail_sensor_speed_mean_m_s": 3.0774270683946944e-05,
  "tail_fk_speed_mean_m_s": 3.12738210005652e-05,
  "peak_tilt_rad": 0.12459530048426704,
  "peak_wheel_torque_nm": 0.7286704778671265,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.31748541302354044,
  "final_integral_m_s": -0.31748541302354044,
  "elapsed_wall_s": 9.534964339982253
}
```
