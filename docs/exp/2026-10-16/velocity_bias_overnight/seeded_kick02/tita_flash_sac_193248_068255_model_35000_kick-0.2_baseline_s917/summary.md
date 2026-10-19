# tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
  "initial_physics_sha256": "c7bc69069951e13b47d0fb78eb950bfe50a89dfa715979eae67888829d8b1537",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.450929968968032,
  "max_drift_m": 8.450929968968032,
  "radial_IAE_m_s": 240.00180004739053,
  "signed_longitudinal_delta_m": 8.36008855599726,
  "tail_speed_mean_m_s": 0.153981365198604,
  "tail_speed_rms_m_s": 0.15398989656627116,
  "tail_sensor_speed_mean_m_s": 0.15364944936437971,
  "tail_fk_speed_mean_m_s": 0.15363309119310223,
  "peak_tilt_rad": 0.07082649056847146,
  "peak_wheel_torque_nm": 1.1725828647613525,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.868391456955578
}
```
