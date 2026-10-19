# tita_flash_sac_193248_068255_model_80000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "4c02bd6e78f49b00179546709068165622ab5d12a72a01c7a6e2a4672f2c120b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.1917755932231797,
  "max_drift_m": 2.1917755932231797,
  "radial_IAE_m_s": 53.82532699151874,
  "signed_longitudinal_delta_m": 2.1901067762992263,
  "tail_speed_mean_m_s": 0.047125542067428756,
  "tail_speed_rms_m_s": 0.047225507747062495,
  "tail_sensor_speed_mean_m_s": 0.046346232673534916,
  "tail_fk_speed_mean_m_s": 0.047114607093229136,
  "peak_tilt_rad": 0.05411350788521996,
  "peak_wheel_torque_nm": 2.9071483612060547,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.724069649004377
}
```
