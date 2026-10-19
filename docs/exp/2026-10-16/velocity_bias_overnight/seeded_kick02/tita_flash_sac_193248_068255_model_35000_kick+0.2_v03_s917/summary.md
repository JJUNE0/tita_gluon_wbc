# tita_flash_sac_193248_068255_model_35000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "233b56a4674605e51eb4bff0e4a6506190276692ba6cffd5893e4ee4728ca731",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01801299855615034,
  "max_drift_m": 0.11467881346138889,
  "radial_IAE_m_s": 1.0652565973798527,
  "signed_longitudinal_delta_m": 0.018010078972738385,
  "tail_speed_mean_m_s": 7.116019118858875e-05,
  "tail_speed_rms_m_s": 7.116268404258765e-05,
  "tail_sensor_speed_mean_m_s": 7.080375030812078e-05,
  "tail_fk_speed_mean_m_s": 6.986115466662188e-05,
  "peak_tilt_rad": 0.08685217385175048,
  "peak_wheel_torque_nm": 1.5926966667175293,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30760749701620177,
  "final_integral_m_s": 0.30760749701620177,
  "elapsed_wall_s": 8.747394535981584
}
```
