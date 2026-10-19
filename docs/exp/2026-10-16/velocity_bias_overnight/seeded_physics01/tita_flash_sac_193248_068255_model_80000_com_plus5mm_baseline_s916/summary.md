# tita_flash_sac_193248_068255_model_80000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "44c8b15ab5ca3fb1bbda0961f21da54fe70229161a64bb424df5063ba9f403be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.28916126636938,
  "max_drift_m": 5.28916126636938,
  "radial_IAE_m_s": 152.7519562687474,
  "signed_longitudinal_delta_m": 5.288936730660911,
  "tail_speed_mean_m_s": 0.09326825733806418,
  "tail_speed_rms_m_s": 0.09331596043946247,
  "tail_sensor_speed_mean_m_s": 0.09302873775185476,
  "tail_fk_speed_mean_m_s": 0.09307692966599472,
  "peak_tilt_rad": 0.05792286767932864,
  "peak_wheel_torque_nm": 1.9788753986358643,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.937063025019597
}
```
