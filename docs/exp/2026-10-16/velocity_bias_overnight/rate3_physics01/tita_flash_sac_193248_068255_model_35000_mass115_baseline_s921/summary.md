# tita_flash_sac_193248_068255_model_35000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "d071c3d1c1987660df7a12f56a2afad78c5c877a8ba52c1402ab09b48b2f4367",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.600495346799758,
  "max_drift_m": 0.600495346799758,
  "radial_IAE_m_s": 20.1159002507558,
  "signed_longitudinal_delta_m": -0.6003830419663363,
  "tail_speed_mean_m_s": -0.007797043115437647,
  "tail_speed_rms_m_s": 0.007820192000090062,
  "tail_sensor_speed_mean_m_s": -0.007780201457104776,
  "tail_fk_speed_mean_m_s": -0.007781423925943123,
  "peak_tilt_rad": 0.050425702132581796,
  "peak_wheel_torque_nm": 0.10038376599550247,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.720074972021393
}
```
