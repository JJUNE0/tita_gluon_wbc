# tita_flash_sac_115632_883848_model_5000_nominal_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_nominal_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "74733ff8ddf92ff485fcbfe79939e4f67636b6dddd47d1fe1fa520d7fddff7ad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04602781869271878,
  "max_drift_m": 0.08781424245421711,
  "radial_IAE_m_s": 2.90627414079082,
  "signed_longitudinal_delta_m": -0.045992532756840315,
  "tail_speed_mean_m_s": 1.8525732419921946e-05,
  "tail_speed_rms_m_s": 1.94675769077422e-05,
  "tail_sensor_speed_mean_m_s": 2.6699132904729624e-05,
  "tail_fk_speed_mean_m_s": 3.057143980545651e-05,
  "peak_tilt_rad": 0.1800316743676489,
  "peak_wheel_torque_nm": 3.32437801361084,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4487370407354131,
  "final_integral_m_s": -0.44877670805805303,
  "elapsed_wall_s": 4.650185488979332
}
```
