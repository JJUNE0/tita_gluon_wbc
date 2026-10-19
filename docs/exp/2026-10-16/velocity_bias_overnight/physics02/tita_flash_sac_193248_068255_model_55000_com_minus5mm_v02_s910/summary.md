# tita_flash_sac_193248_068255_model_55000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "72f0fee3c2e3ef55e5cf7cd150a831ec5946f0d8e64c312e9bfba56c9920461f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02202457362965706,
  "max_drift_m": 0.05461964501428752,
  "radial_IAE_m_s": 1.2149463817495747,
  "signed_longitudinal_delta_m": 0.022021434461134942,
  "tail_speed_mean_m_s": 7.704939203768012e-05,
  "tail_speed_rms_m_s": 7.710269840072806e-05,
  "tail_sensor_speed_mean_m_s": 7.747020300314302e-05,
  "tail_fk_speed_mean_m_s": 7.5689546765514e-05,
  "peak_tilt_rad": 0.12922358053758076,
  "peak_wheel_torque_nm": 0.7471246719360352,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2321418648771782,
  "final_integral_m_s": 0.2319994917621648,
  "elapsed_wall_s": 21.214575305988546
}
```
