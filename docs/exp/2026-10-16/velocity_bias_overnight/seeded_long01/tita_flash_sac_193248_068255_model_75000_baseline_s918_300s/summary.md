# tita_flash_sac_193248_068255_model_75000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "6ddc8383ae5c150daef6b624d38879830e4aba80fa6c2ff11118e2d1bd817420",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 4.1126253986504455,
  "max_drift_m": 17.290181686863104,
  "radial_IAE_m_s": 2500.44383672261,
  "signed_longitudinal_delta_m": -1.9158449896597554,
  "tail_speed_mean_m_s": -0.012402275915221509,
  "tail_speed_rms_m_s": 0.012402276493033278,
  "tail_sensor_speed_mean_m_s": -0.012306727844733877,
  "tail_fk_speed_mean_m_s": -0.012272016544005698,
  "peak_tilt_rad": 0.10223499819980963,
  "peak_wheel_torque_nm": 0.2909107208251953,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 19.061206454003695
}
```
