# tita_flash_sac_193248_068255_model_55000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "9ec3346ee3998014f440dc098a998be55d71a901bcdd66fa38499c85b475b0c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03710110634583808,
  "max_drift_m": 0.09641725032142257,
  "radial_IAE_m_s": 2.11971662670768,
  "signed_longitudinal_delta_m": 0.0371010151713051,
  "tail_speed_mean_m_s": 9.236847224676789e-05,
  "tail_speed_rms_m_s": 9.237716980245562e-05,
  "tail_sensor_speed_mean_m_s": 9.251600397165728e-05,
  "tail_fk_speed_mean_m_s": 9.132729135867505e-05,
  "peak_tilt_rad": 0.14488498708046738,
  "peak_wheel_torque_nm": 0.8930553197860718,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3923016652962754,
  "final_integral_m_s": 0.39211586045341634,
  "elapsed_wall_s": 18.228527861996554
}
```
