# tita_flash_sac_193248_068255_model_80000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "c02fc2f3df862d4dc90cc6d5725fe2b46a2d0287c03f08423dc89f38058e0e15",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0668878890705317,
  "max_drift_m": 0.13341534124026586,
  "radial_IAE_m_s": 3.944946128677948,
  "signed_longitudinal_delta_m": 0.06688513557588144,
  "tail_speed_mean_m_s": 5.8636966859540115e-05,
  "tail_speed_rms_m_s": 5.8846716425684584e-05,
  "tail_sensor_speed_mean_m_s": 5.8153204444487e-05,
  "tail_fk_speed_mean_m_s": 5.9607948726798233e-05,
  "peak_tilt_rad": 0.061703072249633006,
  "peak_wheel_torque_nm": 2.219900369644165,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1819142544222295,
  "final_integral_m_s": 0.1819142544222295,
  "elapsed_wall_s": 12.455710296984762
}
```
