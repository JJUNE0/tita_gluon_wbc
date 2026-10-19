# tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "15f986930088a8302fe1db1be7d943f93b9d3320e43fa23f85b6a6b9c4d14741",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7731712809483835,
  "max_drift_m": 1.7731712809483835,
  "radial_IAE_m_s": 66.66681000717331,
  "signed_longitudinal_delta_m": -0.30730127218723463,
  "tail_speed_mean_m_s": -0.043379339336419645,
  "tail_speed_rms_m_s": 0.04337959831520553,
  "tail_sensor_speed_mean_m_s": -0.043801118027243624,
  "tail_fk_speed_mean_m_s": -0.044064103938830916,
  "peak_tilt_rad": 0.07755217831211292,
  "peak_wheel_torque_nm": 0.7668247222900391,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.146197687019594
}
```
