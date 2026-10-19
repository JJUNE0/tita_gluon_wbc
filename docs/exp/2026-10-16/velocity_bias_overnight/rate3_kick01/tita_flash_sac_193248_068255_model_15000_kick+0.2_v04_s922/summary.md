# tita_flash_sac_193248_068255_model_15000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "746f42e3f4b7b2ac8c90fcdcb32dd1cff2dec717e0e1c87eef47937a94c07bb0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005650007290163763,
  "max_drift_m": 0.041996602412186786,
  "radial_IAE_m_s": 0.10611783099727795,
  "signed_longitudinal_delta_m": 0.0005459839403252144,
  "tail_speed_mean_m_s": -1.1102193257481276e-05,
  "tail_speed_rms_m_s": 1.110493555818211e-05,
  "tail_sensor_speed_mean_m_s": -1.1271888220931499e-05,
  "tail_fk_speed_mean_m_s": -8.957386180038572e-06,
  "peak_tilt_rad": 0.08137716183184773,
  "peak_wheel_torque_nm": 2.5083961486816406,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18252877531169429,
  "final_integral_m_s": -0.18252877531169429,
  "elapsed_wall_s": 7.143960144952871
}
```
