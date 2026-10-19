# tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "57d9c7ea2dafbc50be31e5db26717ba0237b35049d029adfa04b5103856a20e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.09878717844523,
  "max_drift_m": 10.09878717844523,
  "radial_IAE_m_s": 307.54999795688104,
  "signed_longitudinal_delta_m": -9.58343325857263,
  "tail_speed_mean_m_s": -0.16909805184147,
  "tail_speed_rms_m_s": 0.1703273244104686,
  "tail_sensor_speed_mean_m_s": -0.16849743028670283,
  "tail_fk_speed_mean_m_s": -0.16825231013167125,
  "peak_tilt_rad": 0.10031653240237404,
  "peak_wheel_torque_nm": 5.345724582672119,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.971348839986604
}
```
