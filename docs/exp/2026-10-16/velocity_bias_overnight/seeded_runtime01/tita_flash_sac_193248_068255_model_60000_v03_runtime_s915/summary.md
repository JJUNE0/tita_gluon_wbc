# tita_flash_sac_193248_068255_model_60000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "5dcc5d810f3e3a19a0318564acbab7df2f0be4bea3cfc20159442716415ad777",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004685520930857338,
  "max_drift_m": 0.004685520930857338,
  "radial_IAE_m_s": 0.1361202466675245,
  "signed_longitudinal_delta_m": 0.004657417968927096,
  "tail_speed_mean_m_s": 8.600663820445142e-05,
  "tail_speed_rms_m_s": 8.601491264323217e-05,
  "tail_sensor_speed_mean_m_s": 8.565894474274845e-05,
  "tail_fk_speed_mean_m_s": 8.784783282171644e-05,
  "peak_tilt_rad": 0.03884566420025215,
  "peak_wheel_torque_nm": 0.13298894464969635,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.007968420025134364,
  "final_integral_m_s": -0.007968420025134364,
  "elapsed_wall_s": 14.366987164015882
}
```
