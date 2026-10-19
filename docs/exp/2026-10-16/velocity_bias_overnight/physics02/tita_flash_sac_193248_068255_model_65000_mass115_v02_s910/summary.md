# tita_flash_sac_193248_068255_model_65000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "4d46e12f43d48925f1644d421611753b759d88d6a796434439d63fc234f9a56b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03840868761040498,
  "max_drift_m": 0.058582207498500675,
  "radial_IAE_m_s": 2.308121779273259,
  "signed_longitudinal_delta_m": -0.03840538427358095,
  "tail_speed_mean_m_s": 1.4399028792676581e-06,
  "tail_speed_rms_m_s": 1.4411516189327435e-06,
  "tail_sensor_speed_mean_m_s": 1.421793411073523e-06,
  "tail_fk_speed_mean_m_s": 1.847517921509663e-06,
  "peak_tilt_rad": 0.09990701126067658,
  "peak_wheel_torque_nm": 0.653053879737854,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3987430424075572,
  "final_integral_m_s": -0.398746572164916,
  "elapsed_wall_s": 14.89567444397835
}
```
