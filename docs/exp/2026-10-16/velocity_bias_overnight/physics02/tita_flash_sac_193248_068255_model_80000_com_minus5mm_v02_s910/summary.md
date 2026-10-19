# tita_flash_sac_193248_068255_model_80000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "initial_physics_sha256": "a121c4a620ceff53df0955e530a534835910bde2b0276d2e5020241d957b54a1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009487614761846088,
  "max_drift_m": 0.01615405763660394,
  "radial_IAE_m_s": 0.41468262677054313,
  "signed_longitudinal_delta_m": -0.009487144259810981,
  "tail_speed_mean_m_s": -8.365365281307392e-05,
  "tail_speed_rms_m_s": 0.003150812962341269,
  "tail_sensor_speed_mean_m_s": 0.00012880106488107594,
  "tail_fk_speed_mean_m_s": 4.249037148347807e-05,
  "peak_tilt_rad": 0.052241566324844335,
  "peak_wheel_torque_nm": 2.8963286876678467,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.008291211667757425,
  "final_integral_m_s": -0.011684579440076538,
  "elapsed_wall_s": 13.745914137049112
}
```
