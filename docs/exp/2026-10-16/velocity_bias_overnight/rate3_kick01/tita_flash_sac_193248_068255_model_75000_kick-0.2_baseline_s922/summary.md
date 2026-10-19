# tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "7e8027e25c167cc4c0f64f47bcb89915e23035f4ec8d3274fc3237f108eaa4b0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.107494033084754,
  "max_drift_m": 13.107494033084754,
  "radial_IAE_m_s": 392.9128985734083,
  "signed_longitudinal_delta_m": -11.34939748169354,
  "tail_speed_mean_m_s": -0.25591378654791513,
  "tail_speed_rms_m_s": 0.25599427216047,
  "tail_sensor_speed_mean_m_s": -0.25561390461260225,
  "tail_fk_speed_mean_m_s": -0.2556415773226125,
  "peak_tilt_rad": 0.04830134348538939,
  "peak_wheel_torque_nm": 1.6109546422958374,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.40165596298175
}
```
