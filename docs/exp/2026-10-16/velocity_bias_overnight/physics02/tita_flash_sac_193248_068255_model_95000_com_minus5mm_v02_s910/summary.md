# tita_flash_sac_193248_068255_model_95000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "0451442c5c5ba3de94a9f611f17ae46f3380be106184aa440e0293324528765d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.034404222651008565,
  "max_drift_m": 0.07582940675540713,
  "radial_IAE_m_s": 2.0526070540426464,
  "signed_longitudinal_delta_m": -0.03440113700883867,
  "tail_speed_mean_m_s": 1.9337672885393245e-07,
  "tail_speed_rms_m_s": 2.1006118497366381e-07,
  "tail_sensor_speed_mean_m_s": 5.419487060397462e-07,
  "tail_fk_speed_mean_m_s": -1.836555524992521e-07,
  "peak_tilt_rad": 0.09634865206341692,
  "peak_wheel_torque_nm": 0.7075400352478027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3615366116713213,
  "final_integral_m_s": -0.3615362110473772,
  "elapsed_wall_s": 20.569697997998446
}
```
