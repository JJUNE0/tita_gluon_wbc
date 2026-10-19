# tita_flash_sac_193248_068255_model_50000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "10a031c94f1f4b1cbeec3574edf0d7fbbb581b572e5d8fba28679231d6f05bde",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.337164993933237,
  "max_drift_m": 7.337164993933237,
  "radial_IAE_m_s": 214.83574626783505,
  "signed_longitudinal_delta_m": 7.332761327876746,
  "tail_speed_mean_m_s": 0.12756099992033929,
  "tail_speed_rms_m_s": 0.12756406497839953,
  "tail_sensor_speed_mean_m_s": 0.12728531259625847,
  "tail_fk_speed_mean_m_s": 0.1272835532305904,
  "peak_tilt_rad": 0.05851625204490385,
  "peak_wheel_torque_nm": 0.03510481119155884,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.790972727001645
}
```
