# tita_flash_sac_193248_068255_model_75000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.002930404856534424,
  "max_drift_m": 0.05586110124082788,
  "radial_IAE_m_s": 1.5225662627842733,
  "signed_longitudinal_delta_m": -0.0022290358691303127,
  "tail_speed_mean_m_s": 1.0442481467315185e-05,
  "tail_speed_rms_m_s": 1.0442780893057302e-05,
  "tail_sensor_speed_mean_m_s": 1.0418003598345305e-05,
  "tail_fk_speed_mean_m_s": 1.0087858064986879e-05,
  "peak_tilt_rad": 0.08530562547934029,
  "peak_wheel_torque_nm": 0.4399549663066864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2633504743145619,
  "final_integral_m_s": -0.2633504743145619,
  "elapsed_wall_s": 19.232724691974
}
```
