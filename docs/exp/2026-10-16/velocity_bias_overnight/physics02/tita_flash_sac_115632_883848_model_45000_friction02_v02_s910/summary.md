# tita_flash_sac_115632_883848_model_45000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "d8c67fcac4f9d19fa83a02c5fd543f93078ad82abea2d3be2007397ade3e268f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0045853517201452434,
  "max_drift_m": 0.011649323356140492,
  "radial_IAE_m_s": 0.45121720019024314,
  "signed_longitudinal_delta_m": 0.00445940727707409,
  "tail_speed_mean_m_s": -0.0004153332135325638,
  "tail_speed_rms_m_s": 0.010970663746854225,
  "tail_sensor_speed_mean_m_s": -5.918033005862196e-05,
  "tail_fk_speed_mean_m_s": 3.273540654781986e-05,
  "peak_tilt_rad": 0.046496027456151445,
  "peak_wheel_torque_nm": 4.353890419006348,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.007132754093502995,
  "final_integral_m_s": 0.025212086504750292,
  "elapsed_wall_s": 11.63581081898883
}
```
