# tita_flash_sac_193248_068255_model_55000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "aaf3593a3fa24da2b744f13004d07a9dd4ff31a05b96efc5e60242faf09fe69b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 19.129520055383082,
  "max_drift_m": 19.129520055383082,
  "radial_IAE_m_s": 571.1863688792075,
  "signed_longitudinal_delta_m": 18.757701040966644,
  "tail_speed_mean_m_s": 0.3240989154617616,
  "tail_speed_rms_m_s": 0.3240989156351531,
  "tail_sensor_speed_mean_m_s": 0.323398115738782,
  "tail_fk_speed_mean_m_s": 0.3233914166889003,
  "peak_tilt_rad": 0.17354809861718334,
  "peak_wheel_torque_nm": 0.12354004383087158,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.664540352008771
}
```
