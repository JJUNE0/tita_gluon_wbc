# tita_flash_sac_193248_068255_model_35000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "ac2a56d5ad33df4cdef7334a234e24dbf471e03ce6b46bec8bcc8d4fd426fe96",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016334928009435024,
  "max_drift_m": 0.04048616020944831,
  "radial_IAE_m_s": 0.867151775558281,
  "signed_longitudinal_delta_m": 0.016333758943314243,
  "tail_speed_mean_m_s": 7.12637275536461e-05,
  "tail_speed_rms_m_s": 7.126573320229123e-05,
  "tail_sensor_speed_mean_m_s": 7.09095736479214e-05,
  "tail_fk_speed_mean_m_s": 6.996898849295663e-05,
  "peak_tilt_rad": 0.058029571357632426,
  "peak_wheel_torque_nm": 0.5643448233604431,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30728638612265297,
  "final_integral_m_s": 0.30728638612265297,
  "elapsed_wall_s": 12.454067036043853
}
```
