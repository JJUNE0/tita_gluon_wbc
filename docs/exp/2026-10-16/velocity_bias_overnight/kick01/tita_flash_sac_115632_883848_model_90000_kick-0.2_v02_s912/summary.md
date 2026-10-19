# tita_flash_sac_115632_883848_model_90000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "273e729b1c9eb4ae5e3549759cf55f45183d038feb2679eaceba15f5f14ce57d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03679663073718894,
  "max_drift_m": 0.0447428848765082,
  "radial_IAE_m_s": 2.119833336918728,
  "signed_longitudinal_delta_m": 0.03679615743552083,
  "tail_speed_mean_m_s": 3.4509220651726536e-05,
  "tail_speed_rms_m_s": 3.51086329596597e-05,
  "tail_sensor_speed_mean_m_s": 3.4148578502830965e-05,
  "tail_fk_speed_mean_m_s": 3.5321333167107844e-05,
  "peak_tilt_rad": 0.07663495339943305,
  "peak_wheel_torque_nm": 1.9591103792190552,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.39323276896267306,
  "final_integral_m_s": 0.39314125943503636,
  "elapsed_wall_s": 17.11899709800491
}
```
