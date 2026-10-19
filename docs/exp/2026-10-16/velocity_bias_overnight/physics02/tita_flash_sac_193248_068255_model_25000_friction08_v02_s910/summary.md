# tita_flash_sac_193248_068255_model_25000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "initial_physics_sha256": "3f0864853e5edd674da2b1a81476efa1a7327b51028f3b693f67cbc6790220f2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.034500256348653356,
  "max_drift_m": 0.07648995645426487,
  "radial_IAE_m_s": 2.147022577596478,
  "signed_longitudinal_delta_m": 0.034499722347302114,
  "tail_speed_mean_m_s": -2.7501266784716002e-05,
  "tail_speed_rms_m_s": 2.7505192447612854e-05,
  "tail_sensor_speed_mean_m_s": -2.689071519404909e-05,
  "tail_fk_speed_mean_m_s": -2.695259667658453e-05,
  "peak_tilt_rad": 0.10832080896230112,
  "peak_wheel_torque_nm": 1.1446592807769775,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.36795336076056473,
  "final_integral_m_s": 0.36800671041101624,
  "elapsed_wall_s": 16.69480239204131
}
```
