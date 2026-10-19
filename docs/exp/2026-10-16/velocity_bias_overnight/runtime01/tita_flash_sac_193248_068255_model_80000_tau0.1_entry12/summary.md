# tita_flash_sac_193248_068255_model_80000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
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
  "initial_physics_sha256": "7d8f4134b4c87943adce10f90aed6d399de3f0d4a786eb795905f2fbeff74b1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015850609891746536,
  "max_drift_m": 0.015850609891746536,
  "radial_IAE_m_s": 0.6067626046720322,
  "signed_longitudinal_delta_m": 0.015844302963908177,
  "tail_speed_mean_m_s": 0.00028410939746569013,
  "tail_speed_rms_m_s": 0.0012818961083095163,
  "tail_sensor_speed_mean_m_s": 0.0006233741256741392,
  "tail_fk_speed_mean_m_s": 0.00030793802161476825,
  "peak_tilt_rad": 0.05001475761590113,
  "peak_wheel_torque_nm": 2.3872432708740234,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18523848671056278,
  "final_integral_m_s": 0.18519519206401916,
  "elapsed_wall_s": 18.550792085996363
}
```
