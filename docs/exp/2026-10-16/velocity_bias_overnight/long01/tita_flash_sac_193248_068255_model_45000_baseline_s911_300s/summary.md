# tita_flash_sac_193248_068255_model_45000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "9c8f42bd32a9f2428a0e00d6973b5e36eb0b1276649da7cb7bd8dc7af98ed253",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 19.54600820966165,
  "max_drift_m": 27.282118224139566,
  "radial_IAE_m_s": 5282.540668915726,
  "signed_longitudinal_delta_m": -3.8137505693119436,
  "tail_speed_mean_m_s": -0.2059110679500043,
  "tail_speed_rms_m_s": 0.20591145078008202,
  "tail_sensor_speed_mean_m_s": -0.20547948464877186,
  "tail_fk_speed_mean_m_s": -0.2055570900518097,
  "peak_tilt_rad": 0.039773322809052214,
  "peak_wheel_torque_nm": 0.19177982211112976,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 53.50892664695857
}
```
