# tita_flash_sac_115632_883848_model_20000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "88c1af92f8787b590df36af036aadcfa7f7c620befc34543467813aff624e11d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027156634095038212,
  "max_drift_m": 0.12007853988493185,
  "radial_IAE_m_s": 1.6348238101591566,
  "signed_longitudinal_delta_m": 0.02711379118790836,
  "tail_speed_mean_m_s": 3.317816123084969e-05,
  "tail_speed_rms_m_s": 0.002672707420534722,
  "tail_sensor_speed_mean_m_s": -0.00014905490817908182,
  "tail_fk_speed_mean_m_s": 1.2307177853719283e-05,
  "peak_tilt_rad": 0.17020670190445975,
  "peak_wheel_torque_nm": 1.3432246446609497,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2957595642687774,
  "final_integral_m_s": 0.33923136253885433,
  "elapsed_wall_s": 4.886750561010558
}
```
