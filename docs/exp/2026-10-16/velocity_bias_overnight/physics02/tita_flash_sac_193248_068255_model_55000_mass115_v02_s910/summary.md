# tita_flash_sac_193248_068255_model_55000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "2c8417944188812f2f941db0204beb23889b702532ca6bc9c9df8827103ede28",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024247997909364195,
  "max_drift_m": 0.04168997502156804,
  "radial_IAE_m_s": 1.3808156020282474,
  "signed_longitudinal_delta_m": 0.024247077712138233,
  "tail_speed_mean_m_s": 4.677682174058515e-05,
  "tail_speed_rms_m_s": 4.683075306940356e-05,
  "tail_sensor_speed_mean_m_s": 4.6770054655892857e-05,
  "tail_fk_speed_mean_m_s": 4.608739279476768e-05,
  "peak_tilt_rad": 0.16844165746329542,
  "peak_wheel_torque_nm": 0.7583714723587036,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.25175891865160543,
  "final_integral_m_s": 0.25165845174321755,
  "elapsed_wall_s": 20.05095446103951
}
```
