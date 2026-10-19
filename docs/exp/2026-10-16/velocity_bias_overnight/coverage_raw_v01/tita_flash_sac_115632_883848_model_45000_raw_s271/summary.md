# tita_flash_sac_115632_883848_model_45000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
    "estimator": "raw"
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
  "initial_physics_sha256": "1e341932e907edb3417654067358817072b326163eacf5fa2e19147d324278c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012501263956405334,
  "max_drift_m": 0.015775896212151537,
  "radial_IAE_m_s": 0.4928252761210584,
  "signed_longitudinal_delta_m": -0.011898460472403413,
  "tail_speed_mean_m_s": -0.0003808956855726029,
  "tail_speed_rms_m_s": 0.017579544732681918,
  "tail_sensor_speed_mean_m_s": -0.0008152228377606514,
  "tail_fk_speed_mean_m_s": -0.00027647284701905206,
  "peak_tilt_rad": 0.05113185032168821,
  "peak_wheel_torque_nm": 3.2026283740997314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28675889400423965,
  "final_integral_m_s": 0.2627926169002343,
  "elapsed_wall_s": 4.406401194981299
}
```
