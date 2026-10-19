# tita_flash_sac_193248_068255_model_35000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "557d78a5a525dd271e7562d9a023543a1fa2e2f183ef98928767439c30d8639f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029881860925607403,
  "max_drift_m": 0.04405097682961093,
  "radial_IAE_m_s": 1.7395799703822057,
  "signed_longitudinal_delta_m": 0.0298814319593553,
  "tail_speed_mean_m_s": 2.9163657679243292e-05,
  "tail_speed_rms_m_s": 2.9164419429972518e-05,
  "tail_sensor_speed_mean_m_s": 2.8901944267974396e-05,
  "tail_fk_speed_mean_m_s": 2.7964068840794405e-05,
  "peak_tilt_rad": 0.058415380669730954,
  "peak_wheel_torque_nm": 0.43077221512794495,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3073888303781472,
  "final_integral_m_s": 0.3073338843965336,
  "elapsed_wall_s": 5.963272586988751
}
```
