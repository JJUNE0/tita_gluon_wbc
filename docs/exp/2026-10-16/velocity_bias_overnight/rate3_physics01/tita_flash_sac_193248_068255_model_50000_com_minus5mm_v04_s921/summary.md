# tita_flash_sac_193248_068255_model_50000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "5373b468ab8a0413cbe28b88729343d7869c6c4cabe819cd00a3802b282a9bb1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12535347727668333,
  "max_drift_m": 0.12535347727668333,
  "radial_IAE_m_s": 6.911720940914666,
  "signed_longitudinal_delta_m": 0.12535347727405674,
  "tail_speed_mean_m_s": 0.00011382348131962992,
  "tail_speed_rms_m_s": 0.00011431638614098074,
  "tail_sensor_speed_mean_m_s": 0.0001132779020372206,
  "tail_fk_speed_mean_m_s": 0.0001145666052727872,
  "peak_tilt_rad": 0.043965550496142036,
  "peak_wheel_torque_nm": 0.33968448638916016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6466486311330237,
  "final_integral_m_s": 0.6466486311330237,
  "elapsed_wall_s": 9.792438154050615
}
```
