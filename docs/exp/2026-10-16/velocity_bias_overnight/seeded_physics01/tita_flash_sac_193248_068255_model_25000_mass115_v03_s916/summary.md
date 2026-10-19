# tita_flash_sac_193248_068255_model_25000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "a48a9e930ff54f3c5772a252bab75b973274b90e182890185f6e5e6f36d7b822",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02514669180325333,
  "max_drift_m": 0.034959045537611796,
  "radial_IAE_m_s": 1.3209192485742682,
  "signed_longitudinal_delta_m": -0.025142888453326476,
  "tail_speed_mean_m_s": -0.00010238437595889967,
  "tail_speed_rms_m_s": 0.00010262908576233575,
  "tail_sensor_speed_mean_m_s": -0.0001011871558872163,
  "tail_fk_speed_mean_m_s": -0.0001016655498293027,
  "peak_tilt_rad": 0.10893773446109467,
  "peak_wheel_torque_nm": 0.6587285995483398,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09125256079543442,
  "final_integral_m_s": 0.09125256079543442,
  "elapsed_wall_s": 10.651051116001327
}
```
