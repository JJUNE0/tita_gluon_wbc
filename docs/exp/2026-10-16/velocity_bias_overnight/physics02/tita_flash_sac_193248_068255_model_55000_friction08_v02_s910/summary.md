# tita_flash_sac_193248_068255_model_55000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "5f9b793e18f614a38b78772bd24b2ef1fbcea3cc6e5bb852da6855846b7ab9de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02789334738279287,
  "max_drift_m": 0.07219718233077282,
  "radial_IAE_m_s": 1.5626190220623248,
  "signed_longitudinal_delta_m": 0.027892840839531523,
  "tail_speed_mean_m_s": 8.685972412162531e-05,
  "tail_speed_rms_m_s": 8.686508125718348e-05,
  "tail_sensor_speed_mean_m_s": 8.733411318628278e-05,
  "tail_fk_speed_mean_m_s": 8.575857260314081e-05,
  "peak_tilt_rad": 0.13643376522726336,
  "peak_wheel_torque_nm": 0.8219019770622253,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2948460749827771,
  "final_integral_m_s": 0.29467009389454507,
  "elapsed_wall_s": 24.98663433897309
}
```
