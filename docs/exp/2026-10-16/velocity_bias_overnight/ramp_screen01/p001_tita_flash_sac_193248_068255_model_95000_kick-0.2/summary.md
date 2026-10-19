# p001_tita_flash_sac_193248_068255_model_95000_kick-0.2

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_193248_068255_model_95000_kick-0.2",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.05,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "9bad2fd21e173e5fa762c31013a3ba0187843391a383957e787ef9bba8406ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012415088567905451,
  "max_drift_m": 0.20477856640838096,
  "radial_IAE_m_s": 1.6328469900782276,
  "signed_longitudinal_delta_m": 0.012296881711637685,
  "tail_speed_mean_m_s": -5.96843172001907e-06,
  "tail_speed_rms_m_s": 5.880749292699669e-05,
  "tail_sensor_speed_mean_m_s": -6.2214352057027154e-06,
  "tail_fk_speed_mean_m_s": -6.335750617269877e-06,
  "peak_tilt_rad": 0.12868447658518978,
  "peak_wheel_torque_nm": 1.7928608655929565,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23674932056684772,
  "final_integral_m_s": -0.23674932056684772,
  "elapsed_wall_s": 11.126292022992857
}
```
