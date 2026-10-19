# tita_flash_sac_115632_883848_model_5000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "b69f7fbb3add9131f65d639500576b4c7be037de34eb1be016b26525837717f7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007350544552936739,
  "max_drift_m": 0.12368370752542619,
  "radial_IAE_m_s": 0.7591196593875957,
  "signed_longitudinal_delta_m": 0.007273171629174496,
  "tail_speed_mean_m_s": -9.768746975986591e-06,
  "tail_speed_rms_m_s": 0.001267822592867369,
  "tail_sensor_speed_mean_m_s": -1.1680108539688639e-05,
  "tail_fk_speed_mean_m_s": 3.0182522473379234e-06,
  "peak_tilt_rad": 0.19827154928221757,
  "peak_wheel_torque_nm": 5.394992828369141,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45255794064447,
  "final_integral_m_s": -0.45255794064447,
  "elapsed_wall_s": 10.033569691004232
}
```
