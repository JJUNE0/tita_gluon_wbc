# tita_flash_sac_193248_068255_model_20000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "03224a388386a65d37250023bc8fe57eae3bc033876bc3a05bbe636d62a2d038",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06491857638412088,
  "max_drift_m": 0.09688274974225992,
  "radial_IAE_m_s": 3.947817315052437,
  "signed_longitudinal_delta_m": 0.06491113100283456,
  "tail_speed_mean_m_s": -2.6158193331752394e-05,
  "tail_speed_rms_m_s": 2.6160797073505994e-05,
  "tail_sensor_speed_mean_m_s": -1.2169171024968135e-05,
  "tail_fk_speed_mean_m_s": -3.686576087393121e-06,
  "peak_tilt_rad": 0.15674949312101227,
  "peak_wheel_torque_nm": 1.5943628549575806,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6888498698567432,
  "final_integral_m_s": 0.6888574519173817,
  "elapsed_wall_s": 19.06960445997538
}
```
