# tita_flash_sac_193248_068255_model_55000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "3aa168e7d97b644b7b86a35e92a72ed2e36e9144c437227cdf1f22418ffd7876",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024340802731915495,
  "max_drift_m": 0.07434269595752602,
  "radial_IAE_m_s": 1.8800239571735002,
  "signed_longitudinal_delta_m": -0.024338531152187273,
  "tail_speed_mean_m_s": 0.00021654017135124497,
  "tail_speed_rms_m_s": 0.0002165556225647933,
  "tail_sensor_speed_mean_m_s": 0.00021675220879449408,
  "tail_fk_speed_mean_m_s": 0.00021517589796720058,
  "peak_tilt_rad": 0.13614976451104877,
  "peak_wheel_torque_nm": 0.8285545706748962,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29282911847824816,
  "final_integral_m_s": 0.29282911847824816,
  "elapsed_wall_s": 10.935098409012426
}
```
