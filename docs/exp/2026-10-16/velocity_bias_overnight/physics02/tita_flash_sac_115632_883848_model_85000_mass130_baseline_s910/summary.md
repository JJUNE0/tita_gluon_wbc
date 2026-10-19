# tita_flash_sac_115632_883848_model_85000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "0423ae5935ec55a4ab0b84d1e8dd19439684b7c029379a649e6d0cff88e1e29a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.95029674599444,
  "max_drift_m": 7.95029674599444,
  "radial_IAE_m_s": 238.79739854172942,
  "signed_longitudinal_delta_m": -7.94608518779661,
  "tail_speed_mean_m_s": -0.13206806723049377,
  "tail_speed_rms_m_s": 0.13206820073284267,
  "tail_sensor_speed_mean_m_s": -0.13178644142079973,
  "tail_fk_speed_mean_m_s": -0.1317856256853924,
  "peak_tilt_rad": 0.06271894631685893,
  "peak_wheel_torque_nm": 0.4973595142364502,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.800268804014195
}
```
