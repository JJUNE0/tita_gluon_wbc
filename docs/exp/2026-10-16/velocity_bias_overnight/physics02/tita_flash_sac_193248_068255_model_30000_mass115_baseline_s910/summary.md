# tita_flash_sac_193248_068255_model_30000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "8797b97f63282afd1703e1a901bf3e8890c52640cfbc7bdc32534aa41c157de8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.201174595566429,
  "max_drift_m": 4.201174595566429,
  "radial_IAE_m_s": 124.86961407153618,
  "signed_longitudinal_delta_m": -4.185158651494132,
  "tail_speed_mean_m_s": -0.07135638307336628,
  "tail_speed_rms_m_s": 0.07135689398182171,
  "tail_sensor_speed_mean_m_s": -0.07120167813302146,
  "tail_fk_speed_mean_m_s": -0.07119782280948313,
  "peak_tilt_rad": 0.010237592565560893,
  "peak_wheel_torque_nm": 0.13511237502098083,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.392259552958421
}
```
