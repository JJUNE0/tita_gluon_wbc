# tita_flash_sac_115632_883848_model_50000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.511208483643709,
  "max_drift_m": 0.511208483643709,
  "radial_IAE_m_s": 15.786497334487409,
  "signed_longitudinal_delta_m": -0.5001578266473085,
  "tail_speed_mean_m_s": -0.008169620589959221,
  "tail_speed_rms_m_s": 0.008169710692381949,
  "tail_sensor_speed_mean_m_s": -0.008151799316450601,
  "tail_fk_speed_mean_m_s": -0.0081491990139886,
  "peak_tilt_rad": 0.03535388844704079,
  "peak_wheel_torque_nm": 0.2811816930770874,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.711832458036952
}
```
