# tita_flash_sac_115632_883848_model_75000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "3ec39d3c7d030d2d25842cd6e1363a861585f0f5117009e05820226dbe8941a6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.6476017817988864,
  "max_drift_m": 1.6476017817988864,
  "radial_IAE_m_s": 46.97421102130316,
  "signed_longitudinal_delta_m": 1.6475745011454117,
  "tail_speed_mean_m_s": 0.02949559481749624,
  "tail_speed_rms_m_s": 0.029496384970500764,
  "tail_sensor_speed_mean_m_s": 0.029431666770444107,
  "tail_fk_speed_mean_m_s": 0.029431270996084904,
  "peak_tilt_rad": 0.057651559149256126,
  "peak_wheel_torque_nm": 0.16165071725845337,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.212794214021415
}
```
