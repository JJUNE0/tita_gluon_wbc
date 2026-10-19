# tita_flash_sac_193248_068255_model_40000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "initial_physics_sha256": "2668b8f80bf8e6f9c59807f09254d3d1b0c71eb21ee836a23a892848712b74b1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.35581704539724,
  "max_drift_m": 10.35581704539724,
  "radial_IAE_m_s": 307.18927512314383,
  "signed_longitudinal_delta_m": 10.29009507643885,
  "tail_speed_mean_m_s": 0.17812887430152308,
  "tail_speed_rms_m_s": 0.1781295708595884,
  "tail_sensor_speed_mean_m_s": 0.17774458799848045,
  "tail_fk_speed_mean_m_s": 0.17773559066562505,
  "peak_tilt_rad": 0.1358730566901707,
  "peak_wheel_torque_nm": 1.2942132949829102,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.884349258965813
}
```
