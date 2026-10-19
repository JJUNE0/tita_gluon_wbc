# tita_flash_sac_193248_068255_model_35000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.016444360801416584,
  "max_drift_m": 0.04033302569947069,
  "radial_IAE_m_s": 0.871076599441581,
  "signed_longitudinal_delta_m": 0.01644316257574889,
  "tail_speed_mean_m_s": 7.147774164240262e-05,
  "tail_speed_rms_m_s": 7.147910757296815e-05,
  "tail_sensor_speed_mean_m_s": 7.113098737733421e-05,
  "tail_fk_speed_mean_m_s": 7.019262290323815e-05,
  "peak_tilt_rad": 0.05787413694533816,
  "peak_wheel_torque_nm": 0.5621961355209351,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30660878424811355,
  "final_integral_m_s": 0.30660878424811355,
  "elapsed_wall_s": 7.388842304004356
}
```
