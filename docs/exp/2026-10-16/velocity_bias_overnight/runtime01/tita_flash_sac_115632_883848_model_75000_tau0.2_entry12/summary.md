# tita_flash_sac_115632_883848_model_75000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "10114f20f4a7337db81ec3c281cb4c28c0a1e8cfc2df5a265a978d2c3873f988",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0011842335128028503,
  "max_drift_m": 0.017333847252235482,
  "radial_IAE_m_s": 0.0752674841638759,
  "signed_longitudinal_delta_m": 0.0010745636433695913,
  "tail_speed_mean_m_s": 9.375356218767509e-06,
  "tail_speed_rms_m_s": 9.482979625886615e-06,
  "tail_sensor_speed_mean_m_s": 9.412249341737264e-06,
  "tail_fk_speed_mean_m_s": 1.0071070572429242e-05,
  "peak_tilt_rad": 0.06312101122642488,
  "peak_wheel_torque_nm": 0.25266119837760925,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004806977196124388,
  "final_integral_m_s": 0.00478503691439365,
  "elapsed_wall_s": 5.833270133007318
}
```
