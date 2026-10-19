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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "final_drift_m": 0.018005681238326326,
  "max_drift_m": 0.13470816047030842,
  "radial_IAE_m_s": 1.3190593522626302,
  "signed_longitudinal_delta_m": -0.018004301920435135,
  "tail_speed_mean_m_s": 3.3791753570501554e-05,
  "tail_speed_rms_m_s": 3.379566935939507e-05,
  "tail_sensor_speed_mean_m_s": 3.3284883139460055e-05,
  "tail_fk_speed_mean_m_s": 3.467903425622817e-05,
  "peak_tilt_rad": 0.08814694559325709,
  "peak_wheel_torque_nm": 1.832261562347412,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18714504875347932,
  "final_integral_m_s": -0.18714504875347932,
  "elapsed_wall_s": 10.226825576974079
}
```
