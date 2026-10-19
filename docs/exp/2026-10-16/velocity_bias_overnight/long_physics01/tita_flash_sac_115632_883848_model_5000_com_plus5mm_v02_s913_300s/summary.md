# tita_flash_sac_115632_883848_model_5000_com_plus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "f05b2a32cd66439a7c3ed981ab578ef10dec11d2f3cd0ca490cf37d00c0d5878",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.03928696996835261,
  "max_drift_m": 0.08336392132491893,
  "radial_IAE_m_s": 11.955342376541985,
  "signed_longitudinal_delta_m": -0.03921742845223994,
  "tail_speed_mean_m_s": -1.6179194177722215e-06,
  "tail_speed_rms_m_s": 6.8275759471910506e-06,
  "tail_sensor_speed_mean_m_s": 2.0528647940341016e-05,
  "tail_fk_speed_mean_m_s": 6.204189769147511e-06,
  "peak_tilt_rad": 0.17855132901557313,
  "peak_wheel_torque_nm": 2.7618391513824463,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.37020026211353896,
  "final_integral_m_s": -0.3702250548831085,
  "elapsed_wall_s": 87.75635613297345
}
```
