# tita_flash_sac_115632_883848_model_45000_mass130_b-0.250

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_b-0.250",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 120.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": -0.25,
      "limit": 2.0,
      "slew": 2.0,
      "ramp": 0.25
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
  "duration_s": 120.0,
  "final_drift_m": 5.556995010184578,
  "max_drift_m": 6.025716698413727,
  "radial_IAE_m_s": 420.9179471936342,
  "signed_longitudinal_delta_m": -4.7241454184263,
  "tail_speed_mean_m_s": -0.06292799306993205,
  "tail_speed_rms_m_s": 0.06332611488731227,
  "tail_sensor_speed_mean_m_s": -0.062356123834629636,
  "tail_fk_speed_mean_m_s": -0.06255233967743994,
  "peak_tilt_rad": 0.06747942132438811,
  "peak_wheel_torque_nm": 2.2032551765441895,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.25,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 28.628235164040234
}
```
