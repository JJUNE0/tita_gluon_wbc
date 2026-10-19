# tita_flash_sac_115632_883848_model_95000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "5ac49c58b610659d64633779d4cd42c54995ca3adc000a95d9becd44ec2413f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05992372256287746,
  "max_drift_m": 0.1003208780148854,
  "radial_IAE_m_s": 3.645197699894787,
  "signed_longitudinal_delta_m": -0.05992372104019538,
  "tail_speed_mean_m_s": 1.8425950812676843e-05,
  "tail_speed_rms_m_s": 1.8449015298317137e-05,
  "tail_sensor_speed_mean_m_s": 1.8391881388802384e-05,
  "tail_fk_speed_mean_m_s": 1.833318669444843e-05,
  "peak_tilt_rad": 0.1133064050325252,
  "peak_wheel_torque_nm": 0.7703744769096375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5875911657871198,
  "final_integral_m_s": -0.5875911657871198,
  "elapsed_wall_s": 15.906675410980824
}
```
