# p003_tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.05,
      "gain_tau": 0.6,
      "gain_floor": 0.25
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "3a4ba1ca68189c8896b3491841cd28abf61e8aa5305f036f14ac64ec8a9f372d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007307378501913829,
  "max_drift_m": 0.07138197366178936,
  "radial_IAE_m_s": 0.3995818555584958,
  "signed_longitudinal_delta_m": -0.007305143411115935,
  "tail_speed_mean_m_s": -7.386496372020331e-05,
  "tail_speed_rms_m_s": 7.397106576511758e-05,
  "tail_sensor_speed_mean_m_s": -7.330152763673274e-05,
  "tail_fk_speed_mean_m_s": -7.125624858304569e-05,
  "peak_tilt_rad": 0.12854289379896233,
  "peak_wheel_torque_nm": 2.101933002471924,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3506260854822865,
  "final_integral_m_s": -0.35059811742710234,
  "elapsed_wall_s": 13.932657673954964
}
```
