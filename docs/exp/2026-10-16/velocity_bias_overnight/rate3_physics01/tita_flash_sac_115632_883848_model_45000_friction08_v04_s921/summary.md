# tita_flash_sac_115632_883848_model_45000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "13ae68319747decf7ea7987d692b4a0a851ab2bb7b198541e7c8551083170a23",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0031567706187084466,
  "max_drift_m": 0.012671205772208479,
  "radial_IAE_m_s": 0.27101476345757186,
  "signed_longitudinal_delta_m": 0.00304871066162488,
  "tail_speed_mean_m_s": -2.8495213437460093e-05,
  "tail_speed_rms_m_s": 0.007374446786043689,
  "tail_sensor_speed_mean_m_s": 0.0005046845304044444,
  "tail_fk_speed_mean_m_s": -6.833761182714977e-05,
  "peak_tilt_rad": 0.03682804341611323,
  "peak_wheel_torque_nm": 2.561215400695801,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.15464744893221952,
  "final_integral_m_s": 0.15464744893221952,
  "elapsed_wall_s": 8.453745645005256
}
```
