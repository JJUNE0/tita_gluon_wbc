# tita_flash_sac_193248_068255_model_10000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "a567200682b2ce8b1d0f45a2e19805450e2c787ee187c97a55b71d77f055b439",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.32542833524370535,
  "max_drift_m": 0.32542833524370535,
  "radial_IAE_m_s": 10.771082338024502,
  "signed_longitudinal_delta_m": -0.3232087726694743,
  "tail_speed_mean_m_s": -0.004430035425927615,
  "tail_speed_rms_m_s": 0.004438128387472486,
  "tail_sensor_speed_mean_m_s": -0.004408762749280162,
  "tail_fk_speed_mean_m_s": -0.004402975272889021,
  "peak_tilt_rad": 0.024262367371069623,
  "peak_wheel_torque_nm": 0.8744750022888184,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.793497557984665
}
```
