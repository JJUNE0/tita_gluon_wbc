# tita_flash_sac_193248_068255_model_55000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
    "estimator": "fk"
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
  "initial_physics_sha256": "e05782efc51cdaf16eaf3ff2b21bf3977bc0bdfdfbb28ec8685a022657b1cb2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03159526737110469,
  "max_drift_m": 0.1655986346709407,
  "radial_IAE_m_s": 1.9137345343137737,
  "signed_longitudinal_delta_m": 0.03159489814031328,
  "tail_speed_mean_m_s": 7.802554965857098e-05,
  "tail_speed_rms_m_s": 7.805384461893074e-05,
  "tail_sensor_speed_mean_m_s": 7.760396666914583e-05,
  "tail_fk_speed_mean_m_s": 7.669254886376235e-05,
  "peak_tilt_rad": 0.16522899424834625,
  "peak_wheel_torque_nm": 1.4696781635284424,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.35213953907910217,
  "final_integral_m_s": 0.3519859230607082,
  "elapsed_wall_s": 4.284096521034371
}
```
