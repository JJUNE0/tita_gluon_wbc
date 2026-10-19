# tita_flash_sac_193248_068255_model_60000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "1f01636b2db5cfcf53fa0cc5331f5bca6df658977315d59ef15ef45bacb894e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.785563229416241,
  "max_drift_m": 1.785563229416241,
  "radial_IAE_m_s": 55.61921750427272,
  "signed_longitudinal_delta_m": -1.7810866333046014,
  "tail_speed_mean_m_s": -0.027568940874351498,
  "tail_speed_rms_m_s": 0.027575752638813268,
  "tail_sensor_speed_mean_m_s": -0.02750856509596442,
  "tail_fk_speed_mean_m_s": -0.027504693636037907,
  "peak_tilt_rad": 0.028117762337508623,
  "peak_wheel_torque_nm": 0.06950023770332336,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.06817859801231
}
```
