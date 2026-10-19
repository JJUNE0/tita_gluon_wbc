# tita_flash_sac_193248_068255_model_35000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "c0f1be4a2f3c249f876fc9a2f391890eafa12de818cd4c75789069e274c07e37",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.391928278760865,
  "max_drift_m": 8.391928278760865,
  "radial_IAE_m_s": 240.88758723476644,
  "signed_longitudinal_delta_m": 8.35496312999558,
  "tail_speed_mean_m_s": 0.15192894448476962,
  "tail_speed_rms_m_s": 0.15194140058885713,
  "tail_sensor_speed_mean_m_s": 0.15160115899904836,
  "tail_fk_speed_mean_m_s": 0.15158518824684203,
  "peak_tilt_rad": 0.07053785242843391,
  "peak_wheel_torque_nm": 0.12566614151000977,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.635626867995597
}
```
