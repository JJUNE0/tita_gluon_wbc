# tita_flash_sac_193248_068255_model_70000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "fbb91a77f94663190743d3493d38173b921d3686d5339a24bd96ed626c1c79d6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008403787339962243,
  "max_drift_m": 0.010300858981357047,
  "radial_IAE_m_s": 0.4535915031431273,
  "signed_longitudinal_delta_m": 0.008403764557229116,
  "tail_speed_mean_m_s": 2.6247042930536023e-05,
  "tail_speed_rms_m_s": 2.6394871234819455e-05,
  "tail_sensor_speed_mean_m_s": 2.6325213619382376e-05,
  "tail_fk_speed_mean_m_s": 2.6060273379971494e-05,
  "peak_tilt_rad": 0.07526171477593357,
  "peak_wheel_torque_nm": 0.1109587550163269,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08580209346924196,
  "final_integral_m_s": 0.08575439205523717,
  "elapsed_wall_s": 14.588240961020347
}
```
