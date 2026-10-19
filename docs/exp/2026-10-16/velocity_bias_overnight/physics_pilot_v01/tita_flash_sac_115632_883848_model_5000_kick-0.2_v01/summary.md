# tita_flash_sac_115632_883848_model_5000_kick-0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "d222ecc696e8bd0c0400baed13c865b28075d2985658c6708bfb7582915d5def",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05325063941069554,
  "max_drift_m": 0.12813787252422523,
  "radial_IAE_m_s": 3.3162878354412886,
  "signed_longitudinal_delta_m": -0.053241810595977754,
  "tail_speed_mean_m_s": 1.8518036150018198e-05,
  "tail_speed_rms_m_s": 1.981069776396045e-05,
  "tail_sensor_speed_mean_m_s": 3.0339838140496668e-05,
  "tail_fk_speed_mean_m_s": 3.469097321877318e-05,
  "peak_tilt_rad": 0.17622756731878053,
  "peak_wheel_torque_nm": 4.683532238006592,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45696839033150294,
  "final_integral_m_s": -0.45701451799551696,
  "elapsed_wall_s": 4.753069373022299
}
```
