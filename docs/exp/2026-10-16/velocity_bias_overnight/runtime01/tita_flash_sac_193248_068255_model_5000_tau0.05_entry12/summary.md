# tita_flash_sac_193248_068255_model_5000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "030201fa3b21b5354a747d36bebfc6d240c1bcb20e0aec575b9ba9828655fb08",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09980081914302658,
  "max_drift_m": 0.10099443669795706,
  "radial_IAE_m_s": 5.879184135453,
  "signed_longitudinal_delta_m": -0.09977710645059955,
  "tail_speed_mean_m_s": 2.130266747413982e-05,
  "tail_speed_rms_m_s": 2.1307757175905326e-05,
  "tail_sensor_speed_mean_m_s": 1.6442737834684927e-05,
  "tail_fk_speed_mean_m_s": 1.0755054316723526e-05,
  "peak_tilt_rad": 0.07519715374169245,
  "peak_wheel_torque_nm": 0.9687686562538147,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0132927560471559,
  "final_integral_m_s": -1.0133163574179744,
  "elapsed_wall_s": 6.6903423860203475
}
```
