# tita_flash_sac_115632_883848_model_10000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "eb336a14820e7984ab2ad89d5240ba19a41ee4891e94a23eccc46038201b47f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4670548785830428,
  "max_drift_m": 1.4670548785830428,
  "radial_IAE_m_s": 47.098521246734116,
  "signed_longitudinal_delta_m": 1.4662853403711065,
  "tail_speed_mean_m_s": 0.02203233571654657,
  "tail_speed_rms_m_s": 0.02433821447091427,
  "tail_sensor_speed_mean_m_s": 0.02312614389533114,
  "tail_fk_speed_mean_m_s": 0.02174804500186298,
  "peak_tilt_rad": 0.12942968570554125,
  "peak_wheel_torque_nm": 5.54391622543335,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.243400303996168
}
```
