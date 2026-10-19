# tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
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
  "initial_physics_sha256": "92e156d8018c080405033a898fde938b70a5e5180d69ba5e82b907b346fa81ca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.47272207068532,
  "max_drift_m": 8.47272207068532,
  "radial_IAE_m_s": 240.8312594815501,
  "signed_longitudinal_delta_m": 8.376328136718824,
  "tail_speed_mean_m_s": 0.15419008258597366,
  "tail_speed_rms_m_s": 0.15419823092470106,
  "tail_sensor_speed_mean_m_s": 0.15385774298203989,
  "tail_fk_speed_mean_m_s": 0.15384134310373254,
  "peak_tilt_rad": 0.07085514230800682,
  "peak_wheel_torque_nm": 1.1717193126678467,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.551686283026356
}
```
