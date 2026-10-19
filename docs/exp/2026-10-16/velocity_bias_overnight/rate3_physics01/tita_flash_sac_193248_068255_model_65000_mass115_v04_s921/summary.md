# tita_flash_sac_193248_068255_model_65000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "276cbace27a761dbf3349ebaeabc7f19c6720fa31846172977ac3ee59efadf58",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013847562300474006,
  "max_drift_m": 0.06531800918480787,
  "radial_IAE_m_s": 0.9059597511814329,
  "signed_longitudinal_delta_m": -0.013837937525904006,
  "tail_speed_mean_m_s": 5.566334721937617e-06,
  "tail_speed_rms_m_s": 5.61116010788639e-06,
  "tail_sensor_speed_mean_m_s": 5.514137697007713e-06,
  "tail_fk_speed_mean_m_s": 5.988896630968881e-06,
  "peak_tilt_rad": 0.10229153587756867,
  "peak_wheel_torque_nm": 0.8979742527008057,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4019341151516367,
  "final_integral_m_s": -0.4019341151516367,
  "elapsed_wall_s": 9.713557052018587
}
```
