# tita_flash_sac_193248_068255_model_25000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "ede83f4fc7e4bef3e71628edf442d719a5898b25b14dc4b9bae658fc530ed5ed",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022758338322271747,
  "max_drift_m": 0.08137407722121115,
  "radial_IAE_m_s": 1.8322548179629103,
  "signed_longitudinal_delta_m": 0.02271382974212534,
  "tail_speed_mean_m_s": -0.00035018983582134637,
  "tail_speed_rms_m_s": 0.031106911943759304,
  "tail_sensor_speed_mean_m_s": -0.0005416066117522186,
  "tail_fk_speed_mean_m_s": -0.00018644474937540918,
  "peak_tilt_rad": 0.10853319235487469,
  "peak_wheel_torque_nm": 1.5997244119644165,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.17053372243810605,
  "final_integral_m_s": 0.3097894238622243,
  "elapsed_wall_s": 4.41128633194603
}
```
