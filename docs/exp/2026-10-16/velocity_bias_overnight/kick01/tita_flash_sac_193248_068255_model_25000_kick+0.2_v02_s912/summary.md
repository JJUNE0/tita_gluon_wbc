# tita_flash_sac_193248_068255_model_25000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "b9f4e2b0167360c84e21423117cf3c94c082a54caded7add206827ee56e676aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0354411695473693,
  "max_drift_m": 0.14884657406435028,
  "radial_IAE_m_s": 2.2870745528668253,
  "signed_longitudinal_delta_m": 0.035424528662824015,
  "tail_speed_mean_m_s": -2.7230337123087498e-05,
  "tail_speed_rms_m_s": 2.7232125110002635e-05,
  "tail_sensor_speed_mean_m_s": -2.6618743062560695e-05,
  "tail_fk_speed_mean_m_s": -2.6696663057795454e-05,
  "peak_tilt_rad": 0.12653052021856892,
  "peak_wheel_torque_nm": 2.0880963802337646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.36289276669910747,
  "final_integral_m_s": 0.36294433389057384,
  "elapsed_wall_s": 16.55040668701986
}
```
