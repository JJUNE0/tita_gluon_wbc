# tita_flash_sac_193248_068255_model_60000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "initial_physics_sha256": "34ef357e300d56e0a8d158333a400732cae3851032fe0e8a1fdf5c48b3d19bf5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.07470029491372,
  "max_drift_m": 11.07470029491372,
  "radial_IAE_m_s": 332.40651425749894,
  "signed_longitudinal_delta_m": -10.987334403096847,
  "tail_speed_mean_m_s": -0.18497759141308034,
  "tail_speed_rms_m_s": 0.18497773945579135,
  "tail_sensor_speed_mean_m_s": -0.18458374532028476,
  "tail_fk_speed_mean_m_s": -0.18457819586344235,
  "peak_tilt_rad": 0.0364060638586059,
  "peak_wheel_torque_nm": 0.6598132252693176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.245345361006912
}
```
