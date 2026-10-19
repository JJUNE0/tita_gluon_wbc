# tita_flash_sac_193248_068255_model_15000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "c9a7b937fe79d3bfdd309fa8dce7bd48369f5ca16e53d99cec209f5db0a3d127",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04690349546536876,
  "max_drift_m": 0.05401945520507392,
  "radial_IAE_m_s": 2.8399908805354483,
  "signed_longitudinal_delta_m": -0.046903379078517396,
  "tail_speed_mean_m_s": 3.1024089355290955e-05,
  "tail_speed_rms_m_s": 3.121966946383551e-05,
  "tail_sensor_speed_mean_m_s": 3.151449729342476e-05,
  "tail_fk_speed_mean_m_s": 3.4380093574138726e-05,
  "peak_tilt_rad": 0.13242558730961873,
  "peak_wheel_torque_nm": 2.6568048000335693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3388762648422308,
  "final_integral_m_s": -0.3388762648422308,
  "elapsed_wall_s": 10.03435302496655
}
```
