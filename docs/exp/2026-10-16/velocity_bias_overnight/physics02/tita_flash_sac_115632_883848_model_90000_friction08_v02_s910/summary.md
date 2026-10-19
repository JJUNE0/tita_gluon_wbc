# tita_flash_sac_115632_883848_model_90000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "49fa6dfc847339872b2a144c5a0c3b442b40e952b01ceea29751089fc1cd6db1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03762754926360465,
  "max_drift_m": 0.047448292220348666,
  "radial_IAE_m_s": 2.18477605888014,
  "signed_longitudinal_delta_m": 0.03762670567297075,
  "tail_speed_mean_m_s": 4.525185433998758e-05,
  "tail_speed_rms_m_s": 4.767214745187455e-05,
  "tail_sensor_speed_mean_m_s": 4.479288221808259e-05,
  "tail_fk_speed_mean_m_s": 4.605551438623975e-05,
  "peak_tilt_rad": 0.07005313559983661,
  "peak_wheel_torque_nm": 0.45345538854599,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3849345235819453,
  "final_integral_m_s": 0.3848607599925001,
  "elapsed_wall_s": 16.62444637902081
}
```
