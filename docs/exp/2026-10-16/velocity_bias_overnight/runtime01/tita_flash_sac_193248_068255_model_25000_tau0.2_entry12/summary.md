# tita_flash_sac_193248_068255_model_25000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "236c8fb221bb3946c5fb0176a81deec57ee73a9180b6490ad7d24a053db2a3c1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03415632917663169,
  "max_drift_m": 0.07941472298753233,
  "radial_IAE_m_s": 2.1238118375397805,
  "signed_longitudinal_delta_m": 0.03415610506915034,
  "tail_speed_mean_m_s": -2.733027097824896e-05,
  "tail_speed_rms_m_s": 2.733103844614681e-05,
  "tail_sensor_speed_mean_m_s": -2.671823236243984e-05,
  "tail_fk_speed_mean_m_s": -2.6789717898816153e-05,
  "peak_tilt_rad": 0.10855405011823205,
  "peak_wheel_torque_nm": 0.9150463342666626,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3642303492622907,
  "final_integral_m_s": 0.36428310036012135,
  "elapsed_wall_s": 5.868973636010196
}
```
