# tita_flash_sac_115632_883848_model_75000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "087e9bc177c263d1aa16ec81b50baa43cb0220aacced01890ac67cb18e6687a1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026935748540272322,
  "max_drift_m": 0.049390710860637926,
  "radial_IAE_m_s": 2.1948153107078436,
  "signed_longitudinal_delta_m": -0.026919232194091612,
  "tail_speed_mean_m_s": 0.0004483231520925199,
  "tail_speed_rms_m_s": 0.0005142021461326816,
  "tail_sensor_speed_mean_m_s": 0.00044751016717469605,
  "tail_fk_speed_mean_m_s": 0.00044795991192504036,
  "peak_tilt_rad": 0.05201645591208237,
  "peak_wheel_torque_nm": 0.17045727372169495,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.810829455032945
}
```
