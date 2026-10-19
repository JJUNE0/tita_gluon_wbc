# tita_flash_sac_193248_068255_model_35000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "29fd6174ff36d74cceea60c8041f68a1cafd5f28ee4f337f627fe7cd8c56b12b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0033868861780015124,
  "max_drift_m": 0.04975621858145676,
  "radial_IAE_m_s": 0.23878997783215544,
  "signed_longitudinal_delta_m": 0.0033763615607979294,
  "tail_speed_mean_m_s": 1.1285996490103915e-05,
  "tail_speed_rms_m_s": 1.1286282544969123e-05,
  "tail_sensor_speed_mean_m_s": 9.358356770351803e-06,
  "tail_fk_speed_mean_m_s": 6.900962912517038e-06,
  "peak_tilt_rad": 0.06827879829876982,
  "peak_wheel_torque_nm": 0.7967301607131958,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3447163553322212,
  "final_integral_m_s": 0.3447163553322212,
  "elapsed_wall_s": 9.169131929986179
}
```
