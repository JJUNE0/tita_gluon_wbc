# tita_flash_sac_115632_883848_model_55000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "100e25519b2b6b85dffdd43127bddad2431e512aa7a937dc4898d533d5ff595e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01800156758978308,
  "max_drift_m": 0.045210334207801746,
  "radial_IAE_m_s": 6.1524535697550515,
  "signed_longitudinal_delta_m": 0.017997176887153833,
  "tail_speed_mean_m_s": -5.70925997979318e-06,
  "tail_speed_rms_m_s": 5.718405819880278e-06,
  "tail_sensor_speed_mean_m_s": -6.024410974213872e-06,
  "tail_fk_speed_mean_m_s": -3.5171514595730595e-06,
  "peak_tilt_rad": 0.08957045923174478,
  "peak_wheel_torque_nm": 0.9879592657089233,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.20868727373535706,
  "final_integral_m_s": 0.20869364740523538,
  "elapsed_wall_s": 63.70650580403162
}
```
