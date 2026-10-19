# tita_flash_sac_193248_068255_model_80000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "4c02bd6e78f49b00179546709068165622ab5d12a72a01c7a6e2a4672f2c120b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01712270286084459,
  "max_drift_m": 0.0856255243891427,
  "radial_IAE_m_s": 1.0499319355315244,
  "signed_longitudinal_delta_m": 0.017109474427128773,
  "tail_speed_mean_m_s": 2.3184879983637628e-05,
  "tail_speed_rms_m_s": 2.3279144899359494e-05,
  "tail_sensor_speed_mean_m_s": 2.2769780602985098e-05,
  "tail_fk_speed_mean_m_s": 2.4232328497442204e-05,
  "peak_tilt_rad": 0.08583681114332053,
  "peak_wheel_torque_nm": 3.1328659057617188,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18548864447479788,
  "final_integral_m_s": 0.1854435079382681,
  "elapsed_wall_s": 11.821624818025157
}
```
