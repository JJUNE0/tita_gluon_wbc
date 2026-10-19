# tita_flash_sac_115632_883848_model_10000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "bfde01ea4396657c382e2d1b13d9ae7071c684ef33ceed6bacd827d64e422d73",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02971620206245208,
  "max_drift_m": 0.03489725990012643,
  "radial_IAE_m_s": 1.707055559214032,
  "signed_longitudinal_delta_m": -0.029645928402753662,
  "tail_speed_mean_m_s": 0.00013179274013609137,
  "tail_speed_rms_m_s": 0.03314983407572243,
  "tail_sensor_speed_mean_m_s": 0.0017125375144840368,
  "tail_fk_speed_mean_m_s": 0.0002431880561482754,
  "peak_tilt_rad": 0.136624974994646,
  "peak_wheel_torque_nm": 4.598143577575684,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23840205291809818,
  "final_integral_m_s": -0.23840205291809818,
  "elapsed_wall_s": 10.312394968990702
}
```
