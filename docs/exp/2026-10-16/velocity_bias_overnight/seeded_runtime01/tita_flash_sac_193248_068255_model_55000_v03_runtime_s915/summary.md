# tita_flash_sac_193248_068255_model_55000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "0eda90ad2f22eef156be5a435a96b18f7db594675bb3fa81787fa0af6f1fc40e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023638102579170796,
  "max_drift_m": 0.08028951992131755,
  "radial_IAE_m_s": 1.8408169714201774,
  "signed_longitudinal_delta_m": -0.0236360717906217,
  "tail_speed_mean_m_s": 0.00021062845339358822,
  "tail_speed_rms_m_s": 0.00021077910385452141,
  "tail_sensor_speed_mean_m_s": 0.00021057943113007589,
  "tail_fk_speed_mean_m_s": 0.00020908062118962206,
  "peak_tilt_rad": 0.13867617893052286,
  "peak_wheel_torque_nm": 0.7947867512702942,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3147170092104889,
  "final_integral_m_s": 0.3147170092104889,
  "elapsed_wall_s": 15.965301880030893
}
```
