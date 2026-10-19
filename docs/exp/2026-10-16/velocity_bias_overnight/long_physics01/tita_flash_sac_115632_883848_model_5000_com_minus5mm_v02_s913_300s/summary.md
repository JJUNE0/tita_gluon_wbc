# tita_flash_sac_115632_883848_model_5000_com_minus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_minus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "b1f12e9d3f5e35a086c6de7b2b47c4b5d3e9d97f1606e894c6f937c5daa04b11",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.04816608147893575,
  "max_drift_m": 0.09653052256054782,
  "radial_IAE_m_s": 15.300033090878568,
  "signed_longitudinal_delta_m": -0.04816382717752956,
  "tail_speed_mean_m_s": -1.4024567771745192e-05,
  "tail_speed_rms_m_s": 0.0012594323592344941,
  "tail_sensor_speed_mean_m_s": -2.6093766219912932e-05,
  "tail_fk_speed_mean_m_s": -2.2444248244026468e-06,
  "peak_tilt_rad": 0.18547345392307735,
  "peak_wheel_torque_nm": 3.585918426513672,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4554543302159719,
  "final_integral_m_s": -0.45609216567711053,
  "elapsed_wall_s": 81.42897651798557
}
```
