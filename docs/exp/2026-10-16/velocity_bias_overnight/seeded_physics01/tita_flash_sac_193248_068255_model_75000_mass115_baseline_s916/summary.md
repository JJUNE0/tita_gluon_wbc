# tita_flash_sac_193248_068255_model_75000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "95dec6dfb28fae7f75a08e950c73086f70f2e452ff879cf0b9b87f973956d740",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.345908466423186,
  "max_drift_m": 13.345908466423186,
  "radial_IAE_m_s": 411.3678780286425,
  "signed_longitudinal_delta_m": -10.615523989020932,
  "tail_speed_mean_m_s": -0.28531872951984444,
  "tail_speed_rms_m_s": 0.2855546364986212,
  "tail_sensor_speed_mean_m_s": -0.2848656996747026,
  "tail_fk_speed_mean_m_s": -0.2848996007647305,
  "peak_tilt_rad": 0.06792339388193924,
  "peak_wheel_torque_nm": 0.5660895109176636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.608801797032356
}
```
