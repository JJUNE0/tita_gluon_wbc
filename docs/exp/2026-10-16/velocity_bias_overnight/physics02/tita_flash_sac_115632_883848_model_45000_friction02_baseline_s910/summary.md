# tita_flash_sac_115632_883848_model_45000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.164930677628759,
  "max_drift_m": 0.21199516651682657,
  "radial_IAE_m_s": 9.253537648405672,
  "signed_longitudinal_delta_m": 0.1390044382824893,
  "tail_speed_mean_m_s": 0.005515077554803266,
  "tail_speed_rms_m_s": 0.010732281925680867,
  "tail_sensor_speed_mean_m_s": 0.007093503806352651,
  "tail_fk_speed_mean_m_s": 0.005771394512477744,
  "peak_tilt_rad": 0.0417784093970992,
  "peak_wheel_torque_nm": 3.170166015625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.602860946033616
}
```
