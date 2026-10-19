# tita_flash_sac_115632_883848_model_45000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "2156519d16b882e47db2084f3a193d13ab543f9e868eaa46815f879fb9e65e58",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00460810331928355,
  "max_drift_m": 0.017978126005033925,
  "radial_IAE_m_s": 0.5859804634161732,
  "signed_longitudinal_delta_m": -0.004522364037685375,
  "tail_speed_mean_m_s": -0.00034996045435695437,
  "tail_speed_rms_m_s": 0.009310292817939552,
  "tail_sensor_speed_mean_m_s": 0.00013731174049444464,
  "tail_fk_speed_mean_m_s": 9.559450124624265e-05,
  "peak_tilt_rad": 0.0479148237821132,
  "peak_wheel_torque_nm": 4.064591884613037,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021176944879581182,
  "final_integral_m_s": 0.021176944879581182,
  "elapsed_wall_s": 9.431254428985994
}
```
