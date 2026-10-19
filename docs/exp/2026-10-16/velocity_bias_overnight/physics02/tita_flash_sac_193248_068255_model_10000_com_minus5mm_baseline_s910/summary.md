# tita_flash_sac_193248_068255_model_10000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "94fbf4981b7bd8c4c389e3a3d6752eb085ef6cd5ac13ab9a3115987db4d9a4a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.3254279107048957,
  "max_drift_m": 0.3254279107048957,
  "radial_IAE_m_s": 10.771074884807575,
  "signed_longitudinal_delta_m": -0.32320835434151146,
  "tail_speed_mean_m_s": -0.004430025075062934,
  "tail_speed_rms_m_s": 0.004438118249801649,
  "tail_sensor_speed_mean_m_s": -0.004408754500711117,
  "tail_fk_speed_mean_m_s": -0.004402964644232965,
  "peak_tilt_rad": 0.02426234820901676,
  "peak_wheel_torque_nm": 0.874492347240448,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.314702122996096
}
```
