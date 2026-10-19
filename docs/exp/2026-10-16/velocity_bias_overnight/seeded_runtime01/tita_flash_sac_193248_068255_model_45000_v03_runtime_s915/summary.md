# tita_flash_sac_193248_068255_model_45000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "4352052302a576ccd11d21b120de3904acecd3a254a55f70975fd578ec1a4d01",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006027160306741348,
  "max_drift_m": 0.0427276386991707,
  "radial_IAE_m_s": 0.4797508769309628,
  "signed_longitudinal_delta_m": -0.00602223263061762,
  "tail_speed_mean_m_s": 3.7747716805221925e-05,
  "tail_speed_rms_m_s": 3.7749596875202245e-05,
  "tail_sensor_speed_mean_m_s": 3.8463075427177255e-05,
  "tail_fk_speed_mean_m_s": 3.6006710878677545e-05,
  "peak_tilt_rad": 0.0800044516760281,
  "peak_wheel_torque_nm": 0.45158904790878296,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2059930872374919,
  "final_integral_m_s": -0.2059930872374919,
  "elapsed_wall_s": 16.912084992974997
}
```
