# tita_flash_sac_193248_068255_model_55000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "6eb0aee984306f0bdeb093fb44335ad39da22cbefc7f59a32ad895257199a3d7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.034285543324169256,
  "max_drift_m": 0.19159697663602102,
  "radial_IAE_m_s": 2.083634250167324,
  "signed_longitudinal_delta_m": 0.034285356141651485,
  "tail_speed_mean_m_s": 8.496496503588606e-05,
  "tail_speed_rms_m_s": 8.50124142493064e-05,
  "tail_sensor_speed_mean_m_s": 8.512550795813474e-05,
  "tail_fk_speed_mean_m_s": 8.369063657689347e-05,
  "peak_tilt_rad": 0.16190303547759077,
  "peak_wheel_torque_nm": 1.6938616037368774,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3174970121776915,
  "final_integral_m_s": 0.31732687045259106,
  "elapsed_wall_s": 14.092218692007009
}
```
