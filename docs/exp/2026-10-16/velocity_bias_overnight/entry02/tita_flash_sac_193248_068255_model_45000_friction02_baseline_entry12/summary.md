# tita_flash_sac_193248_068255_model_45000_friction02_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction02_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "6984e21f42d3037e1ef06a0051f43604c4da6d6f9c69b736f1e3a3dcf8cb37ac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.27746336834128,
  "max_drift_m": 6.27746336834128,
  "radial_IAE_m_s": 188.34341753457073,
  "signed_longitudinal_delta_m": -6.2677513255929895,
  "tail_speed_mean_m_s": -0.10309053587093542,
  "tail_speed_rms_m_s": 0.10309642284358043,
  "tail_sensor_speed_mean_m_s": -0.10289783651747984,
  "tail_fk_speed_mean_m_s": -0.10289630267731398,
  "peak_tilt_rad": 0.04505898856004986,
  "peak_wheel_torque_nm": 0.17522037029266357,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.99211584898876
}
```
