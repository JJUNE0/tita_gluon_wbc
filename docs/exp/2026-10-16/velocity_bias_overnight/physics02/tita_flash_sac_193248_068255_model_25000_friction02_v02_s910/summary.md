# tita_flash_sac_193248_068255_model_25000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "initial_physics_sha256": "5cc5dabfe0aca6d9999bd2a9c90dbf18e9a4b8ded9ef1439aca7a040985c462f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022475272495048246,
  "max_drift_m": 0.07136762657669757,
  "radial_IAE_m_s": 1.5409163439193627,
  "signed_longitudinal_delta_m": 0.02245765354888771,
  "tail_speed_mean_m_s": -1.333918849336023e-05,
  "tail_speed_rms_m_s": 2.9200280726828714e-05,
  "tail_sensor_speed_mean_m_s": -5.405777119130292e-06,
  "tail_fk_speed_mean_m_s": -1.194686834759631e-05,
  "peak_tilt_rad": 0.10829914886575365,
  "peak_wheel_torque_nm": 1.4500336647033691,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23720544908574784,
  "final_integral_m_s": 0.23719870731247958,
  "elapsed_wall_s": 14.107951115991455
}
```
