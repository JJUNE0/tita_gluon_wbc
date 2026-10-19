# tita_flash_sac_115632_883848_model_45000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "initial_physics_sha256": "ca24d2fe0b271ecc5b4c1783281e72495f8c419fce400e80339cbb0b2e602451",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004167951075811734,
  "max_drift_m": 0.03613901147202907,
  "radial_IAE_m_s": 0.41861714375415054,
  "signed_longitudinal_delta_m": 0.0036641072977625453,
  "tail_speed_mean_m_s": -0.00010278886748832368,
  "tail_speed_rms_m_s": 0.008989011547092546,
  "tail_sensor_speed_mean_m_s": -0.0007239727666236492,
  "tail_fk_speed_mean_m_s": -0.00015914199280621128,
  "peak_tilt_rad": 0.08425503867663098,
  "peak_wheel_torque_nm": 4.441484451293945,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10597174752278077,
  "final_integral_m_s": 0.13253019440729816,
  "elapsed_wall_s": 11.27973504998954
}
```
