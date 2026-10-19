# tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "02b9a888afb64e51a1c41f788f353700f19598cfaffb7b0c0a6707996fe617f0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.39954660272598325,
  "max_drift_m": 0.39954660272598325,
  "radial_IAE_m_s": 9.760402840818603,
  "signed_longitudinal_delta_m": 0.3831223092231021,
  "tail_speed_mean_m_s": 0.009334905385621595,
  "tail_speed_rms_m_s": 0.009335066536177713,
  "tail_sensor_speed_mean_m_s": 0.009314954416505195,
  "tail_fk_speed_mean_m_s": 0.00931719125322945,
  "peak_tilt_rad": 0.04181296181380123,
  "peak_wheel_torque_nm": 1.3779892921447754,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.850479113985784
}
```
