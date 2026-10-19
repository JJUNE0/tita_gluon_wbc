# tita_flash_sac_193248_068255_model_70000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "4f8eaf8b7f26be00855f7b543a0a45067a2e86d991b72b04bc7af84de0650860",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6137980059050427,
  "max_drift_m": 2.6137980059050427,
  "radial_IAE_m_s": 64.76974322789881,
  "signed_longitudinal_delta_m": 2.6123906763241593,
  "tail_speed_mean_m_s": 0.055675851792485534,
  "tail_speed_rms_m_s": 0.055698645541850896,
  "tail_sensor_speed_mean_m_s": 0.05555601232854608,
  "tail_fk_speed_mean_m_s": 0.055554414543788885,
  "peak_tilt_rad": 0.08390227780267967,
  "peak_wheel_torque_nm": 1.643118143081665,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.767611076997127
}
```
