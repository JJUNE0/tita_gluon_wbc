# tita_flash_sac_193248_068255_model_35000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "6b0c38b13074b51a25d8bda3063891414e33b4ce3ffc3e91dda3603605627ba9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.845574021190975,
  "max_drift_m": 8.845574021190975,
  "radial_IAE_m_s": 258.9398260106484,
  "signed_longitudinal_delta_m": 8.69606882648509,
  "tail_speed_mean_m_s": 0.15597973194337567,
  "tail_speed_rms_m_s": 0.15598439644442427,
  "tail_sensor_speed_mean_m_s": 0.1556435280070321,
  "tail_fk_speed_mean_m_s": 0.15562694890151685,
  "peak_tilt_rad": 0.07109264736623544,
  "peak_wheel_torque_nm": 0.04442489147186279,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.385136427998077
}
```
