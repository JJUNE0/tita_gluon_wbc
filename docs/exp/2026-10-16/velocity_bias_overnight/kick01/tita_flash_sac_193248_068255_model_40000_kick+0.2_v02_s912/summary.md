# tita_flash_sac_193248_068255_model_40000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "45e0be99c57980674f04dc61eda35a09e235ae3f43155c26751cdfd1286a95e8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02600223617093581,
  "max_drift_m": 0.1270616547325043,
  "radial_IAE_m_s": 1.59108518321018,
  "signed_longitudinal_delta_m": 0.026001921596776043,
  "tail_speed_mean_m_s": 3.086455580624403e-05,
  "tail_speed_rms_m_s": 3.087723583527371e-05,
  "tail_sensor_speed_mean_m_s": 3.115496446941409e-05,
  "tail_fk_speed_mean_m_s": 3.053585018226973e-05,
  "peak_tilt_rad": 0.13321909262213683,
  "peak_wheel_torque_nm": 2.1655280590057373,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2609331497644637,
  "final_integral_m_s": 0.2608722214789134,
  "elapsed_wall_s": 17.12586656800704
}
```
