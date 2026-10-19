# tita_flash_sac_115632_883848_model_5000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
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
  "initial_physics_sha256": "40c6cc15c09a62996a0d0a65394972d58e2c12cb9d5933316834715206b8ca86",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04286270837235576,
  "max_drift_m": 0.08445996467476734,
  "radial_IAE_m_s": 2.7132171696551968,
  "signed_longitudinal_delta_m": -0.04284725295816278,
  "tail_speed_mean_m_s": 1.8444858498076798e-05,
  "tail_speed_rms_m_s": 1.9675696781176638e-05,
  "tail_sensor_speed_mean_m_s": 3.0520741536053846e-05,
  "tail_fk_speed_mean_m_s": 3.4847643995918584e-05,
  "peak_tilt_rad": 0.1761800619303302,
  "peak_wheel_torque_nm": 4.300506591796875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45723996873620343,
  "final_integral_m_s": -0.4573230894718155,
  "elapsed_wall_s": 5.188412269984838
}
```
