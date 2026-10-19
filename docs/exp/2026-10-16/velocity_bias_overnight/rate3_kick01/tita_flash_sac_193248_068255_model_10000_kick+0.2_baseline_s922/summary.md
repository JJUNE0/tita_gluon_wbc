# tita_flash_sac_193248_068255_model_10000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "initial_physics_sha256": "53f26d94a80995b9db886d3faa7c265a7cb26603db7c5041d4307d9c6bae2776",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.38715213882104754,
  "max_drift_m": 0.38715213882104754,
  "radial_IAE_m_s": 12.838061980831608,
  "signed_longitudinal_delta_m": 0.3830776878074526,
  "tail_speed_mean_m_s": 0.006170937694669053,
  "tail_speed_rms_m_s": 0.006174364241475065,
  "tail_sensor_speed_mean_m_s": 0.0061786592330802656,
  "tail_fk_speed_mean_m_s": 0.006185783892026028,
  "peak_tilt_rad": 0.04529953416573962,
  "peak_wheel_torque_nm": 2.418729066848755,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.89926881500287
}
```
