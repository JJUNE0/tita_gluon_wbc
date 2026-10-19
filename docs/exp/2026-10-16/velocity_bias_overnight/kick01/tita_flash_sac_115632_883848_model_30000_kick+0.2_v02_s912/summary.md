# tita_flash_sac_115632_883848_model_30000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "a6bf79a1c6ed7634a39280dcc5a50c0ccb73b57d376417e8117fab1a5f929b83",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06220867275595211,
  "max_drift_m": 0.19622964020415157,
  "radial_IAE_m_s": 3.864557155747481,
  "signed_longitudinal_delta_m": 0.06220042026276049,
  "tail_speed_mean_m_s": -4.2574465270028664e-05,
  "tail_speed_rms_m_s": 4.399728915049108e-05,
  "tail_sensor_speed_mean_m_s": -4.3563809531937086e-05,
  "tail_fk_speed_mean_m_s": -4.210667663564147e-05,
  "peak_tilt_rad": 0.1634130855777045,
  "peak_wheel_torque_nm": 2.7073564529418945,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5561742752978388,
  "final_integral_m_s": 0.5562896862500303,
  "elapsed_wall_s": 14.712771433987655
}
```
