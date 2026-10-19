# tita_flash_sac_193248_068255_model_25000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "318a3217be1da0644087458fa938c0f0bfa38f343700f79b9ded54903801cf4e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.06457118942384,
  "max_drift_m": 4.06457118942384,
  "radial_IAE_m_s": 120.29833825094038,
  "signed_longitudinal_delta_m": -4.058403475980957,
  "tail_speed_mean_m_s": -0.06953547069447996,
  "tail_speed_rms_m_s": 0.06953730264243797,
  "tail_sensor_speed_mean_m_s": -0.069386513228783,
  "tail_fk_speed_mean_m_s": -0.06938637750119983,
  "peak_tilt_rad": 0.08804876042194021,
  "peak_wheel_torque_nm": 0.46190232038497925,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.847999721998349
}
```
