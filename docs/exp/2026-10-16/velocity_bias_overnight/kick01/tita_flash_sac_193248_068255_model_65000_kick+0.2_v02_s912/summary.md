# tita_flash_sac_193248_068255_model_65000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "50d66ee861b9e06e16e470a6fdacf63b7e88eba85d81a8eb88830b8dc5d0b091",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016935103879027514,
  "max_drift_m": 0.05323044006264401,
  "radial_IAE_m_s": 1.066813339152429,
  "signed_longitudinal_delta_m": -0.01693222432314001,
  "tail_speed_mean_m_s": 1.2887927999347428e-05,
  "tail_speed_rms_m_s": 1.288966330104354e-05,
  "tail_sensor_speed_mean_m_s": 1.2429459141502429e-05,
  "tail_fk_speed_mean_m_s": 1.3823875670451673e-05,
  "peak_tilt_rad": 0.055123105748076995,
  "peak_wheel_torque_nm": 1.84794020652771,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18686092876531776,
  "final_integral_m_s": -0.186887881105194,
  "elapsed_wall_s": 12.901864987041336
}
```
