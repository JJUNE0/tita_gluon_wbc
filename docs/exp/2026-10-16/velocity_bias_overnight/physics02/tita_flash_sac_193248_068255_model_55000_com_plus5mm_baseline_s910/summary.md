# tita_flash_sac_193248_068255_model_55000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "9ec3346ee3998014f440dc098a998be55d71a901bcdd66fa38499c85b475b0c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 20.94990495168899,
  "max_drift_m": 20.94990495168899,
  "radial_IAE_m_s": 612.263326324468,
  "signed_longitudinal_delta_m": 20.765723624145636,
  "tail_speed_mean_m_s": 0.3623367470819553,
  "tail_speed_rms_m_s": 0.3623367472622584,
  "tail_sensor_speed_mean_m_s": 0.3615528312916489,
  "tail_fk_speed_mean_m_s": 0.3615480175148737,
  "peak_tilt_rad": 0.1812286577362574,
  "peak_wheel_torque_nm": 0.25805461406707764,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.755471790966112
}
```
