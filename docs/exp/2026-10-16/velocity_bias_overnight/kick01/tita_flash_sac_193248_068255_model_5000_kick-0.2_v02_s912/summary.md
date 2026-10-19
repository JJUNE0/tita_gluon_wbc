# tita_flash_sac_193248_068255_model_5000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "c652d91188b8b3969d4a89c942c36e882d0b4a3a3dbf54cedc181f4e21f591d2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.10136557250143818,
  "max_drift_m": 0.10258010035023296,
  "radial_IAE_m_s": 6.062833806033144,
  "signed_longitudinal_delta_m": -0.10135401990298482,
  "tail_speed_mean_m_s": 2.127263734947941e-05,
  "tail_speed_rms_m_s": 2.1278048015924768e-05,
  "tail_sensor_speed_mean_m_s": 1.6622221039788104e-05,
  "tail_fk_speed_mean_m_s": 1.0996600267601832e-05,
  "peak_tilt_rad": 0.08623830348640382,
  "peak_wheel_torque_nm": 4.6416215896606445,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.019742419665057,
  "final_integral_m_s": -1.01976540614339,
  "elapsed_wall_s": 12.977125493984204
}
```
