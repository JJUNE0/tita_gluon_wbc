# tita_flash_sac_193248_068255_model_40000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "c2293c544c820adcf45dda03dd2cae61c2e80bb07308a4d62cb9a8d216ca65af",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.36789608689811,
  "max_drift_m": 10.36789608689811,
  "radial_IAE_m_s": 306.01116600216784,
  "signed_longitudinal_delta_m": 10.257136752616027,
  "tail_speed_mean_m_s": 0.17852977035913148,
  "tail_speed_rms_m_s": 0.1785300910156943,
  "tail_sensor_speed_mean_m_s": 0.17814452216909635,
  "tail_fk_speed_mean_m_s": 0.1781356541306,
  "peak_tilt_rad": 0.12029590523577904,
  "peak_wheel_torque_nm": 0.04227668046951294,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.440131856012158
}
```
