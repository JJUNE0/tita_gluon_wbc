# tita_flash_sac_115632_883848_model_45000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "initial_physics_sha256": "e571a0e9f378049dc8ebb7b11874ef37b83ff0e8cca5a9be30f8fe1a36693848",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004474196926429399,
  "max_drift_m": 0.014544406602583524,
  "radial_IAE_m_s": 0.520920320112969,
  "signed_longitudinal_delta_m": 0.0037242737781945693,
  "tail_speed_mean_m_s": -0.00022878127874526765,
  "tail_speed_rms_m_s": 0.008963553726821265,
  "tail_sensor_speed_mean_m_s": -0.0018897188970324486,
  "tail_fk_speed_mean_m_s": 5.182314625497751e-05,
  "peak_tilt_rad": 0.042470181804978635,
  "peak_wheel_torque_nm": 3.394805431365967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16894238079485402,
  "final_integral_m_s": 0.14785810728637228,
  "elapsed_wall_s": 12.586739997961558
}
```
