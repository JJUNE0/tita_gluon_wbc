# tita_flash_sac_193248_068255_model_90000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "efb4acce87f4d40382f164877b45bde36e21955ae1d8397c16c4840ab7f99b05",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.912332169503436,
  "max_drift_m": 12.912332169503436,
  "radial_IAE_m_s": 377.28662367675383,
  "signed_longitudinal_delta_m": 12.798145808262474,
  "tail_speed_mean_m_s": 0.22330559895927046,
  "tail_speed_rms_m_s": 0.22330584697226388,
  "tail_sensor_speed_mean_m_s": 0.2228362767749988,
  "tail_fk_speed_mean_m_s": 0.22283426711778564,
  "peak_tilt_rad": 0.11193844569154865,
  "peak_wheel_torque_nm": 0.9037679433822632,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.82732559699798
}
```
