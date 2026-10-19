# tita_flash_sac_193248_068255_model_60000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "initial_physics_sha256": "326f8d3d7bbcfeacf692d64f678986b790b36d1afe309a7fd0f2e5ff36f39483",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03054223778694794,
  "max_drift_m": 0.07987710807281923,
  "radial_IAE_m_s": 1.8653435262826652,
  "signed_longitudinal_delta_m": -0.03049008727536366,
  "tail_speed_mean_m_s": -4.1378230267983444e-07,
  "tail_speed_rms_m_s": 4.231623237619187e-07,
  "tail_sensor_speed_mean_m_s": -3.868047906197917e-07,
  "tail_fk_speed_mean_m_s": -2.915480420074878e-07,
  "peak_tilt_rad": 0.17575008159401362,
  "peak_wheel_torque_nm": 1.1488803625106812,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.60002682773675,
  "final_integral_m_s": -0.60002682773675,
  "elapsed_wall_s": 15.91721362498356
}
```
