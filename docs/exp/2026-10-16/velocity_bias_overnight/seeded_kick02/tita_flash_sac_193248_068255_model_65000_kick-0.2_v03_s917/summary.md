# tita_flash_sac_193248_068255_model_65000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "905758fd1bd0ff8e0ef0a481f98bdd5b8c24bbb8e7e2f63ed638542bb1b77ec7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01768251655951661,
  "max_drift_m": 0.13450410877300722,
  "radial_IAE_m_s": 1.30183788863519,
  "signed_longitudinal_delta_m": -0.017681122219082596,
  "tail_speed_mean_m_s": 3.3788647668178057e-05,
  "tail_speed_rms_m_s": 3.379268187228315e-05,
  "tail_sensor_speed_mean_m_s": 3.328277670644342e-05,
  "tail_fk_speed_mean_m_s": 3.467580284031308e-05,
  "peak_tilt_rad": 0.0881996873798565,
  "peak_wheel_torque_nm": 1.8328031301498413,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1871409965929482,
  "final_integral_m_s": -0.1871409965929482,
  "elapsed_wall_s": 13.217647229030263
}
```
