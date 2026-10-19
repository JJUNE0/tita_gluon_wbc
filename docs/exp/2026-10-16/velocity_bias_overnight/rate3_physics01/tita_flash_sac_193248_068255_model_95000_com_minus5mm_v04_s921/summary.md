# tita_flash_sac_193248_068255_model_95000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
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
  "initial_physics_sha256": "f66e80579add47f1935e6e59ce8ed30ed45e1abccfb1e12fe704cde35c963425",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013094663992037498,
  "max_drift_m": 0.12508565670592997,
  "radial_IAE_m_s": 1.2489987544311307,
  "signed_longitudinal_delta_m": 0.013093936680213431,
  "tail_speed_mean_m_s": 0.00018314949089430154,
  "tail_speed_rms_m_s": 0.001420431264562817,
  "tail_sensor_speed_mean_m_s": 0.00019293193305192836,
  "tail_fk_speed_mean_m_s": 0.00018226081884670784,
  "peak_tilt_rad": 0.0965112121748859,
  "peak_wheel_torque_nm": 0.650553822517395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.359150439326528,
  "final_integral_m_s": -0.359150439326528,
  "elapsed_wall_s": 8.351872243045364
}
```
