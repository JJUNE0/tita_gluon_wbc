# tita_flash_sac_193248_068255_model_90000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "4eee35f2ac77cd37f05050e3bfee373a6d617f39b1c5190bccb73c3a9b17e010",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05510488805281271,
  "max_drift_m": 0.060682505780682794,
  "radial_IAE_m_s": 3.0208151287729104,
  "signed_longitudinal_delta_m": 0.05510423351322082,
  "tail_speed_mean_m_s": 9.507664736749755e-05,
  "tail_speed_rms_m_s": 0.00014546307876397099,
  "tail_sensor_speed_mean_m_s": 0.00011775729428474052,
  "tail_fk_speed_mean_m_s": 9.411075125780571e-05,
  "peak_tilt_rad": 0.09576619419941368,
  "peak_wheel_torque_nm": 2.035515069961548,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.552961865830715,
  "final_integral_m_s": 0.5527472941431455,
  "elapsed_wall_s": 18.768117181025445
}
```
