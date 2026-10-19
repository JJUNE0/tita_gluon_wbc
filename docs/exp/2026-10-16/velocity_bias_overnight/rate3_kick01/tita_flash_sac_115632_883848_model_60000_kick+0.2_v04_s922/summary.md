# tita_flash_sac_115632_883848_model_60000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "2d9601b51db8284cda41b0827672db1d38f49da51eda58c30c588fe43739f9c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003985957497200846,
  "max_drift_m": 0.09450850003432798,
  "radial_IAE_m_s": 0.4016065565205929,
  "signed_longitudinal_delta_m": 0.0039849857690391986,
  "tail_speed_mean_m_s": -2.5200224588830104e-05,
  "tail_speed_rms_m_s": 2.5785870815141914e-05,
  "tail_sensor_speed_mean_m_s": -2.523356349089328e-05,
  "tail_fk_speed_mean_m_s": -2.309789715788904e-05,
  "peak_tilt_rad": 0.09637473514132266,
  "peak_wheel_torque_nm": 1.9105865955352783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047351340407817875,
  "final_integral_m_s": 0.047351340407817875,
  "elapsed_wall_s": 8.959690488001797
}
```
