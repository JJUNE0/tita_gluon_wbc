# tita_flash_sac_193248_068255_model_40000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "717b2c3a600437e3ea4d0dd957db5794146b6a7b2be84ec7ed80adb093099917",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023929507982351633,
  "max_drift_m": 0.04130486464635989,
  "radial_IAE_m_s": 1.3773524705681894,
  "signed_longitudinal_delta_m": 0.02392948870102687,
  "tail_speed_mean_m_s": 3.5402831807405274e-05,
  "tail_speed_rms_m_s": 3.548711461971185e-05,
  "tail_sensor_speed_mean_m_s": 3.5730172633868706e-05,
  "tail_fk_speed_mean_m_s": 3.5074915462400707e-05,
  "peak_tilt_rad": 0.10706365348092506,
  "peak_wheel_torque_nm": 0.8834031820297241,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.25177528111888986,
  "final_integral_m_s": 0.25171482332734857,
  "elapsed_wall_s": 14.0810996129876
}
```
