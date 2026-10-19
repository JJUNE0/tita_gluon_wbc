# tita_flash_sac_115632_883848_model_75000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "4f1f929c80d99b2164b11a2cd1cefa8dbb02b836a50a9ec199f5e0ab21f7c061",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.004796266985830935,
  "max_drift_m": 0.016193069680458215,
  "radial_IAE_m_s": 0.7842944112395552,
  "signed_longitudinal_delta_m": 0.004536272323530511,
  "tail_speed_mean_m_s": 1.4592786079451394e-05,
  "tail_speed_rms_m_s": 1.4593503022343072e-05,
  "tail_sensor_speed_mean_m_s": 1.4484826481556206e-05,
  "tail_fk_speed_mean_m_s": 1.5055031082792846e-05,
  "peak_tilt_rad": 0.062072748182375515,
  "peak_wheel_torque_nm": 0.3239290118217468,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04172196334075706,
  "final_integral_m_s": 0.041692411185943676,
  "elapsed_wall_s": 71.22815793001791
}
```
