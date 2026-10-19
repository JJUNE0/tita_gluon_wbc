# tita_flash_sac_193248_068255_model_40000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "dab70020c110211f74afa6d95f764aa33365d653929da6f06002e0d246b58b0f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0006190000860561791,
  "max_drift_m": 0.030592625048473276,
  "radial_IAE_m_s": 0.18367517816064927,
  "signed_longitudinal_delta_m": 0.0006002579665209347,
  "tail_speed_mean_m_s": 9.984739413935872e-05,
  "tail_speed_rms_m_s": 9.987979475216073e-05,
  "tail_sensor_speed_mean_m_s": 0.00010000994703136583,
  "tail_fk_speed_mean_m_s": 9.937342524608845e-05,
  "peak_tilt_rad": 0.10036865950269802,
  "peak_wheel_torque_nm": 0.5818288922309875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.208805497260723,
  "final_integral_m_s": 0.208805497260723,
  "elapsed_wall_s": 10.234448843984865
}
```
