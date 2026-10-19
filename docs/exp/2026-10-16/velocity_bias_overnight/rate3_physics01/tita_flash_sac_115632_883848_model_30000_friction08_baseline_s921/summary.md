# tita_flash_sac_115632_883848_model_30000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "8316ab84b0d57f04a262cbba2c23bc399ada629f659266112f07bd8f09114b3c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.101028370426251,
  "max_drift_m": 14.101028370426251,
  "radial_IAE_m_s": 427.89341927116016,
  "signed_longitudinal_delta_m": 14.089410391735855,
  "tail_speed_mean_m_s": 0.23139611740399707,
  "tail_speed_rms_m_s": 0.23139623420695468,
  "tail_sensor_speed_mean_m_s": 0.23089485252737882,
  "tail_fk_speed_mean_m_s": 0.23089330058268348,
  "peak_tilt_rad": 0.128647313980228,
  "peak_wheel_torque_nm": 0.13434529304504395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.3714009859832
}
```
