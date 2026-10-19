# tita_flash_sac_193248_068255_model_80000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "a121c4a620ceff53df0955e530a534835910bde2b0276d2e5020241d957b54a1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06962576823404631,
  "max_drift_m": 0.12913752335285822,
  "radial_IAE_m_s": 6.215716735129073,
  "signed_longitudinal_delta_m": -0.06960948015058548,
  "tail_speed_mean_m_s": 0.00271519748702657,
  "tail_speed_rms_m_s": 0.003828260900463574,
  "tail_sensor_speed_mean_m_s": 0.0024710836153024967,
  "tail_fk_speed_mean_m_s": 0.002834900567251055,
  "peak_tilt_rad": 0.04913646592302379,
  "peak_wheel_torque_nm": 2.113257884979248,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.888636123971082
}
```
