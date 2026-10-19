# tita_flash_sac_115632_883848_model_50000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "45a0c868ef0e64aa0929720d62a71979a5a01a8a0751d7008237aaea4ca94f00",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003632235124850704,
  "max_drift_m": 0.005405562852593906,
  "radial_IAE_m_s": 0.20880334064376327,
  "signed_longitudinal_delta_m": 0.0029285860029808776,
  "tail_speed_mean_m_s": -8.42684628878659e-07,
  "tail_speed_rms_m_s": 1.1912510964515206e-06,
  "tail_sensor_speed_mean_m_s": -6.592607597610595e-07,
  "tail_fk_speed_mean_m_s": 1.817559957468962e-06,
  "peak_tilt_rad": 0.04290504926296457,
  "peak_wheel_torque_nm": 0.3020397424697876,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.018132377924372892,
  "final_integral_m_s": -0.018132377924372892,
  "elapsed_wall_s": 9.257507774978876
}
```
