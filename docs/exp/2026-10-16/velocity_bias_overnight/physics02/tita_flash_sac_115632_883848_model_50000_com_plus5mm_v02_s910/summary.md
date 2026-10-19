# tita_flash_sac_115632_883848_model_50000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "fb2dcd6eb7e7d8ccdd291dab60fe2d2de9f332181e2d94a6343b48fab011d954",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005288008492304741,
  "max_drift_m": 0.013606858040506962,
  "radial_IAE_m_s": 0.32660884700590864,
  "signed_longitudinal_delta_m": 0.005285263153394619,
  "tail_speed_mean_m_s": -1.4212375661241176e-06,
  "tail_speed_rms_m_s": 1.6949765021096386e-06,
  "tail_sensor_speed_mean_m_s": -1.250263716684509e-06,
  "tail_fk_speed_mean_m_s": 9.902221403624095e-07,
  "peak_tilt_rad": 0.04892425919580434,
  "peak_wheel_torque_nm": 0.48433226346969604,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.061105745526655514,
  "final_integral_m_s": 0.06110661697531048,
  "elapsed_wall_s": 11.62630225502653
}
```
