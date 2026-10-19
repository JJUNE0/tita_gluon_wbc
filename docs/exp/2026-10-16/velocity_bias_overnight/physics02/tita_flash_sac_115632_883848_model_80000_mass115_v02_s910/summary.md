# tita_flash_sac_115632_883848_model_80000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "79a2cc91147d99d01d1f8a12c23d4622cb52e480560960adc7f4123595ea432a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02150294256543702,
  "max_drift_m": 0.025321719960247714,
  "radial_IAE_m_s": 1.2125578156553367,
  "signed_longitudinal_delta_m": 0.021490105510161894,
  "tail_speed_mean_m_s": 4.2401203087097353e-05,
  "tail_speed_rms_m_s": 4.2799348053297915e-05,
  "tail_sensor_speed_mean_m_s": 4.239976232760491e-05,
  "tail_fk_speed_mean_m_s": 4.314418947975442e-05,
  "peak_tilt_rad": 0.08185069780561038,
  "peak_wheel_torque_nm": 0.45342931151390076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2170479497375506,
  "final_integral_m_s": 0.21695581060157193,
  "elapsed_wall_s": 15.733102842990775
}
```
