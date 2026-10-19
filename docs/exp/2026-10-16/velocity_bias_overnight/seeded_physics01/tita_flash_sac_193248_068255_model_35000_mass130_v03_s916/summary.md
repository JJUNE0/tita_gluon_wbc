# tita_flash_sac_193248_068255_model_35000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "a69847207653e7b5143b0db78ecd63382f64677a366dddbb0a2bbb60c9dd3c83",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002438276902579372,
  "max_drift_m": 0.04825581646848411,
  "radial_IAE_m_s": 0.14102760441446296,
  "signed_longitudinal_delta_m": 0.002399231642181332,
  "tail_speed_mean_m_s": 5.062494719374625e-05,
  "tail_speed_rms_m_s": 5.064560508146659e-05,
  "tail_sensor_speed_mean_m_s": 5.036992108715337e-05,
  "tail_fk_speed_mean_m_s": 4.988164227607506e-05,
  "peak_tilt_rad": 0.12745402149608087,
  "peak_wheel_torque_nm": 1.1786288022994995,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35347607741438886,
  "final_integral_m_s": -0.35347607741438886,
  "elapsed_wall_s": 11.234665596974082
}
```
