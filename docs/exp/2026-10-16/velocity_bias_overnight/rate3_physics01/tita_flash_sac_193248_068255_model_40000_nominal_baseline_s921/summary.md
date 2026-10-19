# tita_flash_sac_193248_068255_model_40000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "b2a95b4d172e6295d7990cbd96498736a858874815b1cb07fc009e4a6cfd1b6a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.12657532847072,
  "max_drift_m": 10.12657532847072,
  "radial_IAE_m_s": 294.2670182582973,
  "signed_longitudinal_delta_m": 10.066533248863019,
  "tail_speed_mean_m_s": 0.17797642751732354,
  "tail_speed_rms_m_s": 0.17797729982584376,
  "tail_sensor_speed_mean_m_s": 0.17759251470998885,
  "tail_fk_speed_mean_m_s": 0.17758346024196106,
  "peak_tilt_rad": 0.12025412864477869,
  "peak_wheel_torque_nm": 0.1328110694885254,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.194290032959543
}
```
