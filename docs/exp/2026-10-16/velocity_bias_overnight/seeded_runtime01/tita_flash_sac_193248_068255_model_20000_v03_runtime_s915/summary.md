# tita_flash_sac_193248_068255_model_20000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "c43a8ed7ae8ed10b934e1de7128aaa4251d59e398ce7df7f13e518ee44e774f4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013672184077592563,
  "max_drift_m": 0.08518464566026969,
  "radial_IAE_m_s": 0.9885476146225457,
  "signed_longitudinal_delta_m": 0.013652936138600068,
  "tail_speed_mean_m_s": -3.6220649698003833e-05,
  "tail_speed_rms_m_s": 3.622397786529897e-05,
  "tail_sensor_speed_mean_m_s": -2.245362162282539e-05,
  "tail_fk_speed_mean_m_s": -1.3257706524143781e-05,
  "peak_tilt_rad": 0.1515097810021253,
  "peak_wheel_torque_nm": 1.5599002838134766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.676787557217795,
  "final_integral_m_s": 0.676787557217795,
  "elapsed_wall_s": 13.61544653197052
}
```
