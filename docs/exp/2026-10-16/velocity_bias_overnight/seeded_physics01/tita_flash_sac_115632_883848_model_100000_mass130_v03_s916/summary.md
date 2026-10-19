# tita_flash_sac_115632_883848_model_100000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "63124cd60569871988ab7230943d08bf49d2681d79f71f65490971a359acc1bb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01811577898604716,
  "max_drift_m": 0.0918360362585504,
  "radial_IAE_m_s": 0.6013132026888267,
  "signed_longitudinal_delta_m": -0.01798709081299897,
  "tail_speed_mean_m_s": -0.00047561810749035486,
  "tail_speed_rms_m_s": 0.01855157148775206,
  "tail_sensor_speed_mean_m_s": -0.0006161399756922983,
  "tail_fk_speed_mean_m_s": -6.681827701252369e-05,
  "peak_tilt_rad": 0.19403637334355905,
  "peak_wheel_torque_nm": 5.065060138702393,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.48524175376097706,
  "final_integral_m_s": -0.48524175376097706,
  "elapsed_wall_s": 16.081499398045707
}
```
