# tita_flash_sac_193248_068255_model_60000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "2d25710d520bda118e12050644d5ca55175b5aceab241db17c2a9851fb96c9ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0044073486504943365,
  "max_drift_m": 0.022599351796870594,
  "radial_IAE_m_s": 0.4458299429888715,
  "signed_longitudinal_delta_m": -0.00427732885378852,
  "tail_speed_mean_m_s": 9.33864569906208e-05,
  "tail_speed_rms_m_s": 9.375044139146881e-05,
  "tail_sensor_speed_mean_m_s": 9.277339891111826e-05,
  "tail_fk_speed_mean_m_s": 9.476174567384931e-05,
  "peak_tilt_rad": 0.05075374982553682,
  "peak_wheel_torque_nm": 0.2948523759841919,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.126438631356506,
  "final_integral_m_s": -0.126438631356506,
  "elapsed_wall_s": 12.970850421988871
}
```
