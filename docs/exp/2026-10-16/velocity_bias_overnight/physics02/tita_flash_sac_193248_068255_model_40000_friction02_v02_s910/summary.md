# tita_flash_sac_193248_068255_model_40000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "4b5e043a99525ed2bc070a6a8428b09921510263323de1a79dcc177551f18e0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03127513536984132,
  "max_drift_m": 0.05928815303454466,
  "radial_IAE_m_s": 1.876647640781246,
  "signed_longitudinal_delta_m": 0.031200748198311798,
  "tail_speed_mean_m_s": 6.245299792351185e-06,
  "tail_speed_rms_m_s": 6.304072759278767e-06,
  "tail_sensor_speed_mean_m_s": 6.105896412159448e-06,
  "tail_fk_speed_mean_m_s": 5.418512491801966e-06,
  "peak_tilt_rad": 0.11529237195530273,
  "peak_wheel_torque_nm": 1.3255956172943115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3037284198129101,
  "final_integral_m_s": 0.30371812467737347,
  "elapsed_wall_s": 21.039250975998584
}
```
