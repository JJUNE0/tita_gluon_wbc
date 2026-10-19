# tita_flash_sac_193248_068255_model_60000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "c31150ef304f0702b56cc4dddbcda3657909e9268ba1160b8190b6041984e74f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12097124136867705,
  "max_drift_m": 0.15715249676819854,
  "radial_IAE_m_s": 4.446611046545355,
  "signed_longitudinal_delta_m": -0.12042439254295356,
  "tail_speed_mean_m_s": -0.003267047145544457,
  "tail_speed_rms_m_s": 0.00330623516150664,
  "tail_sensor_speed_mean_m_s": -0.0032598142234473706,
  "tail_fk_speed_mean_m_s": -0.0032578066215950404,
  "peak_tilt_rad": 0.07173371398826212,
  "peak_wheel_torque_nm": 1.4846827983856201,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.857770622998942
}
```
