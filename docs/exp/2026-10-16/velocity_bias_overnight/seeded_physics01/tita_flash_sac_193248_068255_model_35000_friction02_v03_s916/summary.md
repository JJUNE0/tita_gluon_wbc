# tita_flash_sac_193248_068255_model_35000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "4f9d3d51d49c828f265bda0cb3e936fcc7104b376ae97e77ba440f32e3915def",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003388031367415475,
  "max_drift_m": 0.050449957017177895,
  "radial_IAE_m_s": 0.23989567707438647,
  "signed_longitudinal_delta_m": 0.0033775495896073444,
  "tail_speed_mean_m_s": 1.1285292504163726e-05,
  "tail_speed_rms_m_s": 1.1285554026819452e-05,
  "tail_sensor_speed_mean_m_s": 9.357181689206015e-06,
  "tail_fk_speed_mean_m_s": 6.900582373961133e-06,
  "peak_tilt_rad": 0.06827872263346224,
  "peak_wheel_torque_nm": 0.7669336795806885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3447159107707264,
  "final_integral_m_s": 0.3447159107707264,
  "elapsed_wall_s": 10.525401327002328
}
```
