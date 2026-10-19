# tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "233b56a4674605e51eb4bff0e4a6506190276692ba6cffd5893e4ee4728ca731",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.783825419445153,
  "max_drift_m": 8.783825419445153,
  "radial_IAE_m_s": 258.816507325445,
  "signed_longitudinal_delta_m": 8.68936721279303,
  "tail_speed_mean_m_s": 0.15444765803788177,
  "tail_speed_rms_m_s": 0.15445534597234628,
  "tail_sensor_speed_mean_m_s": 0.15411477122381353,
  "tail_fk_speed_mean_m_s": 0.15409834263531244,
  "peak_tilt_rad": 0.08893643691030362,
  "peak_wheel_torque_nm": 1.3998881578445435,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.38257216999773
}
```
