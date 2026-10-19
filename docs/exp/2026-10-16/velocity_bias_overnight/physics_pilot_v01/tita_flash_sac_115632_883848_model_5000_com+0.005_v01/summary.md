# tita_flash_sac_115632_883848_model_5000_com+0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com+0.005_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "891354843f2232381716947dc4f4176d70fb0dabe09bbbf9ba144f92d7fb858f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04264116902861851,
  "max_drift_m": 0.08550789318980728,
  "radial_IAE_m_s": 2.665238543129887,
  "signed_longitudinal_delta_m": -0.04263854226312347,
  "tail_speed_mean_m_s": 1.6830633849868778e-05,
  "tail_speed_rms_m_s": 1.7417386774792874e-05,
  "tail_sensor_speed_mean_m_s": 2.9350566502277538e-05,
  "tail_fk_speed_mean_m_s": 3.404088677593049e-05,
  "peak_tilt_rad": 0.1719374691495137,
  "peak_wheel_torque_nm": 3.9510741233825684,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.39564165245673316,
  "final_integral_m_s": -0.3956996929231965,
  "elapsed_wall_s": 5.473201588029042
}
```
