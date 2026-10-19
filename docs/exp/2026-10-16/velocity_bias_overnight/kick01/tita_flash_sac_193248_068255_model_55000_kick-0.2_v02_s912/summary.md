# tita_flash_sac_193248_068255_model_55000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "345106fa1e5e0f8a3b90b2b8db2ca4395557dd9a005199d9c9fb7939538580dc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027852524581900778,
  "max_drift_m": 0.04248722874942033,
  "radial_IAE_m_s": 1.5180962240602036,
  "signed_longitudinal_delta_m": 0.027851801922332848,
  "tail_speed_mean_m_s": 8.679458260703377e-05,
  "tail_speed_rms_m_s": 8.679921973443298e-05,
  "tail_sensor_speed_mean_m_s": 8.718929744220756e-05,
  "tail_fk_speed_mean_m_s": 8.554134137215338e-05,
  "peak_tilt_rad": 0.13710549433386054,
  "peak_wheel_torque_nm": 1.4986228942871094,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30906995834004763,
  "final_integral_m_s": 0.30890151392723136,
  "elapsed_wall_s": 14.18621976900613
}
```
