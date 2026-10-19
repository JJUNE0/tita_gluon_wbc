# tita_flash_sac_193248_068255_model_80000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "807659b35dd4e22f175f7a6b98e7600f5bd35a0a4c2adea744e8dbd355984ab6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003126691074978149,
  "max_drift_m": 0.016533064998374168,
  "radial_IAE_m_s": 0.3665959343825239,
  "signed_longitudinal_delta_m": 0.0029532825458160146,
  "tail_speed_mean_m_s": -0.00011156303141149431,
  "tail_speed_rms_m_s": 0.0062320650052139735,
  "tail_sensor_speed_mean_m_s": -0.0005472517396009328,
  "tail_fk_speed_mean_m_s": -0.00011358598374645142,
  "peak_tilt_rad": 0.05321461212226386,
  "peak_wheel_torque_nm": 2.451159954071045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.049337416249313294,
  "final_integral_m_s": 0.09903338459061355,
  "elapsed_wall_s": 4.452356559981126
}
```
