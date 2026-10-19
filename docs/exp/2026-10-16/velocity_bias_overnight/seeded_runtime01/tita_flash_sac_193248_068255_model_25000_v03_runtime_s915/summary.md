# tita_flash_sac_193248_068255_model_25000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "initial_physics_sha256": "0ef4e79d94273ac0dde0f3a0dc53f8d1256628be8769550d4a25eaad35baa030",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03559154174160803,
  "max_drift_m": 0.07210260919959682,
  "radial_IAE_m_s": 2.026810080707441,
  "signed_longitudinal_delta_m": -0.035584253276140086,
  "tail_speed_mean_m_s": -6.71817949791127e-05,
  "tail_speed_rms_m_s": 6.718823185327336e-05,
  "tail_sensor_speed_mean_m_s": -6.648462101632408e-05,
  "tail_fk_speed_mean_m_s": -6.656668708256742e-05,
  "peak_tilt_rad": 0.10864709150680185,
  "peak_wheel_torque_nm": 0.9604750871658325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.36294932522566725,
  "final_integral_m_s": 0.36294932522566725,
  "elapsed_wall_s": 14.360331754025538
}
```
