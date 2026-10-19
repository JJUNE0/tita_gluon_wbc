# tita_flash_sac_115632_883848_model_10000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
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
  "final_drift_m": 0.08238275053320998,
  "max_drift_m": 0.11139835111617129,
  "radial_IAE_m_s": 5.88059851399171,
  "signed_longitudinal_delta_m": 0.08237731379264815,
  "tail_speed_mean_m_s": -0.0010922923717038696,
  "tail_speed_rms_m_s": 0.017577326336859808,
  "tail_sensor_speed_mean_m_s": -0.002079748069809314,
  "tail_fk_speed_mean_m_s": -0.001128508271062863,
  "peak_tilt_rad": 0.128879659522674,
  "peak_wheel_torque_nm": 5.546586513519287,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3415250289701558,
  "final_integral_m_s": 0.3415250289701558,
  "elapsed_wall_s": 9.016487047018018
}
```
