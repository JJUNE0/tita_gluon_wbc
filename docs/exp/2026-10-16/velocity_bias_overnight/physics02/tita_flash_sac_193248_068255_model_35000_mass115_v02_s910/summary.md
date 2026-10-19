# tita_flash_sac_193248_068255_model_35000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "d8dc883ecb872982c2345d4d16eeb1306492019b5f40b2a6c635d2ecee83a2b0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005960455587166664,
  "max_drift_m": 0.007629341679682755,
  "radial_IAE_m_s": 0.09541781559291365,
  "signed_longitudinal_delta_m": -0.0005928380058934641,
  "tail_speed_mean_m_s": 3.132167871072492e-05,
  "tail_speed_rms_m_s": 3.13243342187023e-05,
  "tail_sensor_speed_mean_m_s": 3.085287738609951e-05,
  "tail_fk_speed_mean_m_s": 2.9886772279513727e-05,
  "peak_tilt_rad": 0.061228062188255716,
  "peak_wheel_torque_nm": 0.23957085609436035,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.011356859359163167,
  "final_integral_m_s": -0.011414935728964782,
  "elapsed_wall_s": 19.727871427952778
}
```
