# tita_flash_sac_115632_883848_model_5000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "f98b109416fa972bda55ebf801d63b7a0128c7c6710b80e0cf009d8ee212428f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.046027790062019514,
  "max_drift_m": 0.08781424993456229,
  "radial_IAE_m_s": 2.9062741243560133,
  "signed_longitudinal_delta_m": -0.045992504473126666,
  "tail_speed_mean_m_s": 1.852678097275674e-05,
  "tail_speed_rms_m_s": 1.9471890203823654e-05,
  "tail_sensor_speed_mean_m_s": 2.6699497952874958e-05,
  "tail_fk_speed_mean_m_s": 3.0572858028334145e-05,
  "peak_tilt_rad": 0.18003161794254252,
  "peak_wheel_torque_nm": 3.324383497238159,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4487366468731082,
  "final_integral_m_s": -0.4487763731427156,
  "elapsed_wall_s": 6.364068628987297
}
```
