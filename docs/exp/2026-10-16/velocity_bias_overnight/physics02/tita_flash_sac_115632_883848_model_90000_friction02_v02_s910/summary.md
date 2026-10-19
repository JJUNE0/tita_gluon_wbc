# tita_flash_sac_115632_883848_model_90000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "88e9d7342e4de016fde8500c2b04c718c73ae9331a26296fa18b5476dd69d870",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.11859185716587256,
  "max_drift_m": 0.14378678395826372,
  "radial_IAE_m_s": 7.659719548896573,
  "signed_longitudinal_delta_m": 0.11558415015229519,
  "tail_speed_mean_m_s": -0.0006487036727859468,
  "tail_speed_rms_m_s": 0.012710603842228928,
  "tail_sensor_speed_mean_m_s": 7.065745298416945,
  "tail_fk_speed_mean_m_s": 7.06564917412292,
  "peak_tilt_rad": 0.6300530269302347,
  "peak_wheel_torque_nm": 12.0,
  "saturation_fraction": 0.0003333333333333333,
  "final_velocity_bias_m_s": 2.0,
  "final_integral_m_s": 0.15291027921052036,
  "elapsed_wall_s": 17.47417881403817
}
```
