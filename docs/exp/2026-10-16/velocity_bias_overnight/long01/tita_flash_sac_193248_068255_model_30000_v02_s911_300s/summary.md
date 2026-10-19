# tita_flash_sac_193248_068255_model_30000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "ba6028e06d4c50e1c066e3416e783ba12cd607b8b0206ed2b32fa1b6fb317885",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.010105391171404703,
  "max_drift_m": 0.017909091776752754,
  "radial_IAE_m_s": 3.0695058795491175,
  "signed_longitudinal_delta_m": 0.010105390262349455,
  "tail_speed_mean_m_s": 2.160690833095121e-06,
  "tail_speed_rms_m_s": 2.163151071932486e-06,
  "tail_sensor_speed_mean_m_s": 2.1830752971952034e-06,
  "tail_fk_speed_mean_m_s": 2.139211186257381e-06,
  "peak_tilt_rad": 0.019925500419310627,
  "peak_wheel_torque_nm": 0.35442790389060974,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10520025701694714,
  "final_integral_m_s": 0.10519652831671125,
  "elapsed_wall_s": 72.42506407300243
}
```
