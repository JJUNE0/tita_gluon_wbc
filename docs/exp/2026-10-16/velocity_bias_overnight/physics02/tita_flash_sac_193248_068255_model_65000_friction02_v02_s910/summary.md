# tita_flash_sac_193248_068255_model_65000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "985456b0ee02351e499bb72413c138f6504d3c52086b98a538afe20d25075d54",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014541602316258919,
  "max_drift_m": 0.020260867380930123,
  "radial_IAE_m_s": 0.8709942384165044,
  "signed_longitudinal_delta_m": -0.014539261877763623,
  "tail_speed_mean_m_s": -1.8074198661874248e-06,
  "tail_speed_rms_m_s": 1.8077648000597032e-06,
  "tail_sensor_speed_mean_m_s": -1.7806009343160756e-06,
  "tail_fk_speed_mean_m_s": -1.7117955649297945e-06,
  "peak_tilt_rad": 0.04005398593161824,
  "peak_wheel_torque_nm": 0.18138760328292847,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.14885738719031272,
  "final_integral_m_s": -0.14885404465636118,
  "elapsed_wall_s": 17.00031100900378
}
```
