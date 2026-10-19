# tita_flash_sac_115632_883848_model_30000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "a249422fd5cf27bac2ce2ef1ed6d47e716bd48812aa630329ac5a9526aea3476",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017038012394447574,
  "max_drift_m": 0.09240974130976358,
  "radial_IAE_m_s": 1.199178835039195,
  "signed_longitudinal_delta_m": -0.017002643131093547,
  "tail_speed_mean_m_s": 1.4747654347687498e-05,
  "tail_speed_rms_m_s": 1.699169402820933e-05,
  "tail_sensor_speed_mean_m_s": 1.3279328809598933e-05,
  "tail_fk_speed_mean_m_s": 1.5361059180989e-05,
  "peak_tilt_rad": 0.12618143438863605,
  "peak_wheel_torque_nm": 1.4678590297698975,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5292303240365244,
  "final_integral_m_s": 0.5292303240365244,
  "elapsed_wall_s": 10.42242290097056
}
```
