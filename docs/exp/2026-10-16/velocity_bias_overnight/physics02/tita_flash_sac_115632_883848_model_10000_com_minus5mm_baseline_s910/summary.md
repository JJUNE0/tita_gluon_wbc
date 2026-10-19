# tita_flash_sac_115632_883848_model_10000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "d7e9ec4f981f792def6f79de127bd8ce7f0ddb2e454c9fc51e69d164fc6a3916",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9879544543281435,
  "max_drift_m": 0.9879544543281435,
  "radial_IAE_m_s": 31.615073707238484,
  "signed_longitudinal_delta_m": 0.9875280675995844,
  "tail_speed_mean_m_s": 0.014434578695942524,
  "tail_speed_rms_m_s": 0.016343299246263054,
  "tail_sensor_speed_mean_m_s": 0.01414278691167712,
  "tail_fk_speed_mean_m_s": 0.014173027967515982,
  "peak_tilt_rad": 0.10853591687129005,
  "peak_wheel_torque_nm": 2.833129405975342,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.406377570994664
}
```
