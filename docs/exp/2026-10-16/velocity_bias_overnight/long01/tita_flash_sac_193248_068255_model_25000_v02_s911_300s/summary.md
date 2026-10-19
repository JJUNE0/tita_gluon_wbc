# tita_flash_sac_193248_068255_model_25000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "b92d871a4ec6f1bc4a1680891af03515a8a70ed0765925c9b1be587c91ee5bde",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.026537374693255185,
  "max_drift_m": 0.07583394928851545,
  "radial_IAE_m_s": 9.402572609751747,
  "signed_longitudinal_delta_m": 0.026522508676229052,
  "tail_speed_mean_m_s": -4.628226032165183e-05,
  "tail_speed_rms_m_s": 5.013948552627319e-05,
  "tail_sensor_speed_mean_m_s": -4.381297390957044e-05,
  "tail_fk_speed_mean_m_s": -4.275258798677438e-05,
  "peak_tilt_rad": 0.10855407273555029,
  "peak_wheel_torque_nm": 1.134936809539795,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28976048011485805,
  "final_integral_m_s": 0.2899476747911022,
  "elapsed_wall_s": 65.3490948100225
}
```
