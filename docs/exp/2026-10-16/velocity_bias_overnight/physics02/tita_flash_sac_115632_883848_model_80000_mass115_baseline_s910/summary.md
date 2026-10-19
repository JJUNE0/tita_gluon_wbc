# tita_flash_sac_115632_883848_model_80000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 4.46403891769329,
  "max_drift_m": 4.46403891769329,
  "radial_IAE_m_s": 131.75698487067567,
  "signed_longitudinal_delta_m": 4.4542032750368845,
  "tail_speed_mean_m_s": 0.07609803247837683,
  "tail_speed_rms_m_s": 0.07609816320285935,
  "tail_sensor_speed_mean_m_s": 0.07593463191077716,
  "tail_fk_speed_mean_m_s": 0.07593534259059165,
  "peak_tilt_rad": 0.09029386663682071,
  "peak_wheel_torque_nm": 0.4259985685348511,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.584024521987885
}
```
