# tita_flash_sac_193248_068255_model_85000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "46e47b37fe17dd351c7a29d78a751eac23aeed4daf4c9e87be86261c375c9186",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09709740339022753,
  "max_drift_m": 0.12322547753067288,
  "radial_IAE_m_s": 6.322501577645577,
  "signed_longitudinal_delta_m": 0.09185789241697918,
  "tail_speed_mean_m_s": -0.0005121945829618705,
  "tail_speed_rms_m_s": 0.008827511524886032,
  "tail_sensor_speed_mean_m_s": 7.453874707449057,
  "tail_fk_speed_mean_m_s": 7.453861987635731,
  "peak_tilt_rad": 0.6255486650645183,
  "peak_wheel_torque_nm": 9.711441040039062,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.510581595008262
}
```
