# tita_flash_sac_193248_068255_model_40000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "41ed25e1d78909750a3457c93ea0e1c306f1537c63f1a7ccf292e77aaf2df493",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9861620590461493,
  "max_drift_m": 1.9861620590461493,
  "radial_IAE_m_s": 56.526101424693316,
  "signed_longitudinal_delta_m": 1.9851159052019451,
  "tail_speed_mean_m_s": 0.03644006945962149,
  "tail_speed_rms_m_s": 0.036450116529877376,
  "tail_sensor_speed_mean_m_s": 0.03636219495777717,
  "tail_fk_speed_mean_m_s": 0.03635998039656061,
  "peak_tilt_rad": 0.11703276162879628,
  "peak_wheel_torque_nm": 0.11294789612293243,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.830986028013285
}
```
