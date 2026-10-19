# tita_flash_sac_115632_883848_model_30000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "f1e7254b19d2de825cdd8fae2eeb041e0c30987e8001c8a03b7ff1bcb645526e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04397171626883729,
  "max_drift_m": 0.10320671825021575,
  "radial_IAE_m_s": 2.8417644667727022,
  "signed_longitudinal_delta_m": -0.04394978265979779,
  "tail_speed_mean_m_s": 5.26310211927048e-05,
  "tail_speed_rms_m_s": 5.367037971746608e-05,
  "tail_sensor_speed_mean_m_s": 5.242003097875139e-05,
  "tail_fk_speed_mean_m_s": 5.269034952419269e-05,
  "peak_tilt_rad": 0.10689186151673447,
  "peak_wheel_torque_nm": 0.7570830583572388,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4201741172003698,
  "final_integral_m_s": 0.4201741172003698,
  "elapsed_wall_s": 14.901662863965612
}
```
