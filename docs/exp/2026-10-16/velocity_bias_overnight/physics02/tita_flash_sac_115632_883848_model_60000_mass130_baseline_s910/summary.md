# tita_flash_sac_115632_883848_model_60000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "7d7491eeb6b4937c1919ea4e21113b024dad55c0f9683f167fb025b6003e0b93",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.424905545646626,
  "max_drift_m": 9.424905545646626,
  "radial_IAE_m_s": 284.8808195762505,
  "signed_longitudinal_delta_m": -9.372361401201058,
  "tail_speed_mean_m_s": -0.15471405137220068,
  "tail_speed_rms_m_s": 0.15472081496933643,
  "tail_sensor_speed_mean_m_s": -0.15438176759813477,
  "tail_fk_speed_mean_m_s": -0.15437936258429089,
  "peak_tilt_rad": 0.06652040338977239,
  "peak_wheel_torque_nm": 0.25965428352355957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.407432359002996
}
```
