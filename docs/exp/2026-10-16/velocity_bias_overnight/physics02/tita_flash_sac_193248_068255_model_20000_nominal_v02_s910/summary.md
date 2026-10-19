# tita_flash_sac_193248_068255_model_20000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "6371b77413a2f123990b869b7b4f42921a808f25598f35d34a5ca6b8a43a5688",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06354059932008797,
  "max_drift_m": 0.08913828577582608,
  "radial_IAE_m_s": 3.8687673432215286,
  "signed_longitudinal_delta_m": 0.06353998485852894,
  "tail_speed_mean_m_s": -3.017027570854272e-05,
  "tail_speed_rms_m_s": 3.0173705319766795e-05,
  "tail_sensor_speed_mean_m_s": -1.5103244932330412e-05,
  "tail_fk_speed_mean_m_s": -5.465967937978661e-06,
  "peak_tilt_rad": 0.15142460721575968,
  "peak_wheel_torque_nm": 1.6476961374282837,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.675394981040512,
  "final_integral_m_s": 0.6754061844906675,
  "elapsed_wall_s": 14.442291459999979
}
```
