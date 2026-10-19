# tita_flash_sac_193248_068255_model_35000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "final_drift_m": 0.02986119665997206,
  "max_drift_m": 0.03822226184877545,
  "radial_IAE_m_s": 1.7357348669829313,
  "signed_longitudinal_delta_m": 0.029860785545380606,
  "tail_speed_mean_m_s": 2.9176975785337168e-05,
  "tail_speed_rms_m_s": 2.9177667880928434e-05,
  "tail_sensor_speed_mean_m_s": 2.8916519239505896e-05,
  "tail_fk_speed_mean_m_s": 2.797836840144027e-05,
  "peak_tilt_rad": 0.05827889761078442,
  "peak_wheel_torque_nm": 0.6241937279701233,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30732174693802633,
  "final_integral_m_s": 0.3072666768719871,
  "elapsed_wall_s": 5.783543632016517
}
```
