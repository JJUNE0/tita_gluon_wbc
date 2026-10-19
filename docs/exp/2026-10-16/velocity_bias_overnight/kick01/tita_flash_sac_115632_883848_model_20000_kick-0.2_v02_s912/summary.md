# tita_flash_sac_115632_883848_model_20000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "de53ed655bdc430bbae5b06e4e203e698b76328b211467c60495e5bb5cffd802",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022388071365871374,
  "max_drift_m": 0.04955838424548363,
  "radial_IAE_m_s": 1.3534547578156826,
  "signed_longitudinal_delta_m": 0.02238528729901987,
  "tail_speed_mean_m_s": 4.187373782571499e-08,
  "tail_speed_rms_m_s": 4.103432227238057e-06,
  "tail_sensor_speed_mean_m_s": 6.603454531462359e-06,
  "tail_fk_speed_mean_m_s": 1.4369842903895527e-05,
  "peak_tilt_rad": 0.14629332918980875,
  "peak_wheel_torque_nm": 1.2341313362121582,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27015167061960155,
  "final_integral_m_s": 0.27012852661904285,
  "elapsed_wall_s": 15.230000513023697
}
```
