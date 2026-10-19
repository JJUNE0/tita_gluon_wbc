# tita_flash_sac_115632_883848_model_100000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "dfa3a1b01fc42eef074c67242e97108d6d52bfbd805c5e996c8e0e30e1ae3c5f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.937587905516592,
  "max_drift_m": 6.937587905516592,
  "radial_IAE_m_s": 210.67469319175453,
  "signed_longitudinal_delta_m": 6.937187987527,
  "tail_speed_mean_m_s": 0.11276987669932818,
  "tail_speed_rms_m_s": 0.11277083574088187,
  "tail_sensor_speed_mean_m_s": 0.11252549762331647,
  "tail_fk_speed_mean_m_s": 0.11252531155734581,
  "peak_tilt_rad": 0.0896113582493483,
  "peak_wheel_torque_nm": 0.38638317584991455,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.762977909995243
}
```
