# tita_flash_sac_193248_068255_model_25000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "final_drift_m": 0.032841457076853195,
  "max_drift_m": 0.04355797810343071,
  "radial_IAE_m_s": 2.007204985990703,
  "signed_longitudinal_delta_m": 0.03284097570886133,
  "tail_speed_mean_m_s": -2.7368387833890887e-05,
  "tail_speed_rms_m_s": 2.7368894003963323e-05,
  "tail_sensor_speed_mean_m_s": -2.6757490497737815e-05,
  "tail_fk_speed_mean_m_s": -2.6824781766327776e-05,
  "peak_tilt_rad": 0.10855406180307892,
  "peak_wheel_torque_nm": 1.518943190574646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3642293342117149,
  "final_integral_m_s": 0.3642826008614144,
  "elapsed_wall_s": 13.768888638995122
}
```
