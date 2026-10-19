# tita_flash_sac_193248_068255_model_55000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "138467cf451814c60aab717f290ee3ec919dfd1e7247d77652ed364a0a2c41a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027561609185881936,
  "max_drift_m": 0.06173377279528776,
  "radial_IAE_m_s": 2.0465161222201904,
  "signed_longitudinal_delta_m": -0.027559140896951922,
  "tail_speed_mean_m_s": 0.0002158542090441193,
  "tail_speed_rms_m_s": 0.00021586587195057837,
  "tail_sensor_speed_mean_m_s": 0.00021599126646399013,
  "tail_fk_speed_mean_m_s": 0.0002143525467603179,
  "peak_tilt_rad": 0.1369515739495839,
  "peak_wheel_torque_nm": 1.2695550918579102,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30508841198663034,
  "final_integral_m_s": 0.30508841198663034,
  "elapsed_wall_s": 9.58249421598157
}
```
