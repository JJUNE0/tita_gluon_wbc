# tita_flash_sac_115632_883848_model_30000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "initial_physics_sha256": "26a376cc47577621dc20f38a072a5e748c62c4fbf1e1240362aa022dafb41670",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.04078626762817045,
  "max_drift_m": 0.11716097928711276,
  "radial_IAE_m_s": 14.523785937823648,
  "signed_longitudinal_delta_m": 0.04078604470301757,
  "tail_speed_mean_m_s": -5.4972983254913214e-05,
  "tail_speed_rms_m_s": 5.502400807522512e-05,
  "tail_sensor_speed_mean_m_s": -5.523189271213111e-05,
  "tail_fk_speed_mean_m_s": -5.4648662225298716e-05,
  "peak_tilt_rad": 0.1269574884900977,
  "peak_wheel_torque_nm": 1.117516279220581,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.43520392390023427,
  "final_integral_m_s": 0.4353038352064127,
  "elapsed_wall_s": 55.167172449990176
}
```
