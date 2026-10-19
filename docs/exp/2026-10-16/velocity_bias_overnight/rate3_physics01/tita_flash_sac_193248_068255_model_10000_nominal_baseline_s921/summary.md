# tita_flash_sac_193248_068255_model_10000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "d63298c04210c2f2fb78b2ffeec4698430c6aa1841bb935ef7add64d1cc7efab",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.3025274143452722,
  "max_drift_m": 0.3025274143452722,
  "radial_IAE_m_s": 8.284870424998662,
  "signed_longitudinal_delta_m": 0.2979232094178581,
  "tail_speed_mean_m_s": 0.005873836890839899,
  "tail_speed_rms_m_s": 0.005877502443612075,
  "tail_sensor_speed_mean_m_s": 0.0058829064615708165,
  "tail_fk_speed_mean_m_s": 0.0058901869491608016,
  "peak_tilt_rad": 0.024761748022058095,
  "peak_wheel_torque_nm": 0.9040058851242065,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.601031708007213
}
```
