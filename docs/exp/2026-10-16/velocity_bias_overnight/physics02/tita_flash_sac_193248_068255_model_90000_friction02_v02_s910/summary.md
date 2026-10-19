# tita_flash_sac_193248_068255_model_90000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "efb4acce87f4d40382f164877b45bde36e21955ae1d8397c16c4840ab7f99b05",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07238312910709413,
  "max_drift_m": 0.08311285713193872,
  "radial_IAE_m_s": 4.303746003065356,
  "signed_longitudinal_delta_m": 0.07237976208707601,
  "tail_speed_mean_m_s": 5.2786847065740297e-05,
  "tail_speed_rms_m_s": 6.231710936518183e-05,
  "tail_sensor_speed_mean_m_s": -2.482775412285419e-05,
  "tail_fk_speed_mean_m_s": 3.5079760812134444e-05,
  "peak_tilt_rad": 0.0976789518504737,
  "peak_wheel_torque_nm": 3.4366142749786377,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7075790060340325,
  "final_integral_m_s": 0.7076769176111961,
  "elapsed_wall_s": 16.347673561016563
}
```
