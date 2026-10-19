# tita_flash_sac_193248_068255_model_10000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "c4fda80c28318d62943cc3e658941036df7617eaa635bee4dff3cd728c8c19da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7114695925146806,
  "max_drift_m": 1.7114695925146806,
  "radial_IAE_m_s": 52.34695890017512,
  "signed_longitudinal_delta_m": -1.70364418866852,
  "tail_speed_mean_m_s": -0.027592011901760784,
  "tail_speed_rms_m_s": 0.027713038017294415,
  "tail_sensor_speed_mean_m_s": -0.027540843852467543,
  "tail_fk_speed_mean_m_s": -0.027529526630767426,
  "peak_tilt_rad": 0.02719195621762751,
  "peak_wheel_torque_nm": 0.8956372737884521,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.757842171005905
}
```
