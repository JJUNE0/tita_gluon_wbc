# tita_flash_sac_193248_068255_model_25000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "3699a562f542d85ebae2432e503fdca80894cf3da153c552255e3b0ec482f86f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.226953696525985,
  "max_drift_m": 11.226953696525985,
  "radial_IAE_m_s": 334.55724110212395,
  "signed_longitudinal_delta_m": 11.218260982173968,
  "tail_speed_mean_m_s": 0.1876636713222987,
  "tail_speed_rms_m_s": 0.187663759077373,
  "tail_sensor_speed_mean_m_s": 0.18725742241887555,
  "tail_fk_speed_mean_m_s": 0.1872572698119786,
  "peak_tilt_rad": 0.10954559055640001,
  "peak_wheel_torque_nm": 1.5246740579605103,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.809282058035024
}
```
