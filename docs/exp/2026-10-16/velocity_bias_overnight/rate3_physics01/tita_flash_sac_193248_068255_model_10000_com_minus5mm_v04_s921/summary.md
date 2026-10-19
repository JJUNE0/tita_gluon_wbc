# tita_flash_sac_193248_068255_model_10000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "final_drift_m": 0.02681394780103568,
  "max_drift_m": 0.028582123714193344,
  "radial_IAE_m_s": 1.5815979075964566,
  "signed_longitudinal_delta_m": -0.026752171135744608,
  "tail_speed_mean_m_s": 7.054733763938874e-05,
  "tail_speed_rms_m_s": 7.068911615630976e-05,
  "tail_sensor_speed_mean_m_s": 8.859746315872947e-05,
  "tail_fk_speed_mean_m_s": 9.589940921929578e-05,
  "peak_tilt_rad": 0.024239424778653266,
  "peak_wheel_torque_nm": 0.8810766339302063,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.11603341353366052,
  "final_integral_m_s": -0.11603341353366052,
  "elapsed_wall_s": 8.529321558016818
}
```
