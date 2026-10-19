# tita_flash_sac_193248_068255_model_75000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "a088d9920e4741993f6fc45c76402a57f218c0d66ceafe789d11ed216781fc0c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006547883251868241,
  "max_drift_m": 0.05570521687787854,
  "radial_IAE_m_s": 0.5379783712970915,
  "signed_longitudinal_delta_m": -0.006528322888283527,
  "tail_speed_mean_m_s": 3.156768764347661e-05,
  "tail_speed_rms_m_s": 3.161599218346297e-05,
  "tail_sensor_speed_mean_m_s": 3.167160024917059e-05,
  "tail_fk_speed_mean_m_s": 3.123348052389645e-05,
  "peak_tilt_rad": 0.0850683373904586,
  "peak_wheel_torque_nm": 0.44183775782585144,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2799681409623913,
  "final_integral_m_s": -0.2799681409623913,
  "elapsed_wall_s": 12.738415672967676
}
```
