# tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "8c1416b339500c5233c022aa94c9b1ced91a3db92c0e425316044c64012da31d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.163851372577226,
  "max_drift_m": 7.163851372577226,
  "radial_IAE_m_s": 205.72885435816542,
  "signed_longitudinal_delta_m": 7.103799672389221,
  "tail_speed_mean_m_s": 0.12961977322059348,
  "tail_speed_rms_m_s": 0.12962922703961197,
  "tail_sensor_speed_mean_m_s": 0.129340284148279,
  "tail_fk_speed_mean_m_s": 0.12932433532371557,
  "peak_tilt_rad": 0.06524809387725594,
  "peak_wheel_torque_nm": 0.1260383427143097,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.544248457008507
}
```
