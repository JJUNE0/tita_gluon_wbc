# tita_flash_sac_193248_068255_model_65000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "418ef7f02d176e43b994326f12b9563b6da412b481de3d79fa14fb0ec333854a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016774937111903594,
  "max_drift_m": 0.03423407016905131,
  "radial_IAE_m_s": 1.0904942024191693,
  "signed_longitudinal_delta_m": -0.016765142299235525,
  "tail_speed_mean_m_s": 3.50540349723401e-05,
  "tail_speed_rms_m_s": 3.505784064643588e-05,
  "tail_sensor_speed_mean_m_s": 3.449331905498045e-05,
  "tail_fk_speed_mean_m_s": 3.5929700728329956e-05,
  "peak_tilt_rad": 0.048573440311154625,
  "peak_wheel_torque_nm": 0.2352248877286911,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18907468371908323,
  "final_integral_m_s": -0.18907468371908323,
  "elapsed_wall_s": 5.65558677201625
}
```
