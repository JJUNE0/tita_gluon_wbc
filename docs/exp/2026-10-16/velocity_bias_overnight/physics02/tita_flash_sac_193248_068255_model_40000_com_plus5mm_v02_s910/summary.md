# tita_flash_sac_193248_068255_model_40000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "b87cea77a7c531fd9101021c8a2ff2da0807ac0b96399c7658017f60f57780a4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02819955813899928,
  "max_drift_m": 0.05678734441925607,
  "radial_IAE_m_s": 1.6521488979700953,
  "signed_longitudinal_delta_m": 0.028199174483696722,
  "tail_speed_mean_m_s": 2.8506940286475866e-05,
  "tail_speed_rms_m_s": 2.851040569431226e-05,
  "tail_sensor_speed_mean_m_s": 2.8826373954516172e-05,
  "tail_fk_speed_mean_m_s": 2.820845490018437e-05,
  "peak_tilt_rad": 0.11451588317753258,
  "peak_wheel_torque_nm": 0.9880245327949524,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2991496158186613,
  "final_integral_m_s": 0.29909465299513527,
  "elapsed_wall_s": 15.653779685962945
}
```
