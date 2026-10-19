# tita_flash_sac_115632_883848_model_50000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "caf13f8d52a59454ba9731f604b2348293f6c7d4f198d188537972569670558b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0034321242404941558,
  "max_drift_m": 0.005814842663891808,
  "radial_IAE_m_s": 0.1957987497863377,
  "signed_longitudinal_delta_m": -0.0029116551488943846,
  "tail_speed_mean_m_s": -1.5727413531117234e-06,
  "tail_speed_rms_m_s": 2.632013474997148e-06,
  "tail_sensor_speed_mean_m_s": -7.689082535463831e-07,
  "tail_fk_speed_mean_m_s": 1.5089722238428302e-06,
  "peak_tilt_rad": 0.041595965057339646,
  "peak_wheel_torque_nm": 0.29092419147491455,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02135241745363791,
  "final_integral_m_s": 0.02135241745363791,
  "elapsed_wall_s": 8.097524004988372
}
```
