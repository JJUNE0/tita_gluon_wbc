# tita_flash_sac_193248_068255_model_50000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "88ea628bfc3c18cd4051155b18ecead3978d50ef795e018579538f83c95cc8ba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.5981856905625325,
  "max_drift_m": 5.5981856905625325,
  "radial_IAE_m_s": 159.07383434710908,
  "signed_longitudinal_delta_m": 5.5977953208990145,
  "tail_speed_mean_m_s": 0.10203146920350531,
  "tail_speed_rms_m_s": 0.10203977653588495,
  "tail_sensor_speed_mean_m_s": 0.10181099121941412,
  "tail_fk_speed_mean_m_s": 0.10180906692865295,
  "peak_tilt_rad": 0.053447890317488644,
  "peak_wheel_torque_nm": 0.2702094316482544,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.95185868901899
}
```
