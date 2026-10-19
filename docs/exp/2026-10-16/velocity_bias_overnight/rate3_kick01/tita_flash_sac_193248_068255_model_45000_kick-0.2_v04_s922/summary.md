# tita_flash_sac_193248_068255_model_45000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "c5c202688b4d9636143f88875d68dfe834a70a05a9efdcdca473f043a7d56fbd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006520508392944136,
  "max_drift_m": 0.14003254394183945,
  "radial_IAE_m_s": 0.7355555678267787,
  "signed_longitudinal_delta_m": -0.006515083765497436,
  "tail_speed_mean_m_s": 3.8661047092240915e-05,
  "tail_speed_rms_m_s": 3.866461167475439e-05,
  "tail_sensor_speed_mean_m_s": 3.943702730989369e-05,
  "tail_fk_speed_mean_m_s": 3.696617772757085e-05,
  "peak_tilt_rad": 0.11864624134786461,
  "peak_wheel_torque_nm": 1.7008857727050781,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.208164671700941,
  "final_integral_m_s": -0.208164671700941,
  "elapsed_wall_s": 6.637042090005707
}
```
