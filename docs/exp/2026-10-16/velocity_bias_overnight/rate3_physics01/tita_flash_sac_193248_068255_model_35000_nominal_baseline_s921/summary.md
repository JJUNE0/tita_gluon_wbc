# tita_flash_sac_193248_068255_model_35000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
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
  "initial_physics_sha256": "692dd08fca0d2ac7d343e6936bf5019facd014877a90ce65e7657eb7d425cfb6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.612372649691332,
  "max_drift_m": 8.612372649691332,
  "radial_IAE_m_s": 249.1881793968988,
  "signed_longitudinal_delta_m": 8.520525807078924,
  "tail_speed_mean_m_s": 0.1541697784788289,
  "tail_speed_rms_m_s": 0.15417796596571454,
  "tail_sensor_speed_mean_m_s": 0.15383746316869612,
  "tail_fk_speed_mean_m_s": 0.15382108440570075,
  "peak_tilt_rad": 0.07085241845898294,
  "peak_wheel_torque_nm": 0.12793362140655518,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.241330519027542
}
```
