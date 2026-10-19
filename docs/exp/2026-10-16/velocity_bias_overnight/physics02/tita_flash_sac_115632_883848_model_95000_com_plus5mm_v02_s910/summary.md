# tita_flash_sac_115632_883848_model_95000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "7aea6444f1c31129232c09e19c71d40603183bad8d1e2a5f01a1d754747e58c6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018331033369557274,
  "max_drift_m": 0.018331033369557274,
  "radial_IAE_m_s": 0.8657747651196568,
  "signed_longitudinal_delta_m": 0.018330251748658134,
  "tail_speed_mean_m_s": 0.00013530006582252726,
  "tail_speed_rms_m_s": 0.00013537368529199708,
  "tail_sensor_speed_mean_m_s": 0.0001347796100424184,
  "tail_fk_speed_mean_m_s": 0.0001354564575283546,
  "peak_tilt_rad": 0.06246082236728712,
  "peak_wheel_torque_nm": 0.20669105648994446,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18519424258260578,
  "final_integral_m_s": 0.18495424255716514,
  "elapsed_wall_s": 19.118135099997744
}
```
