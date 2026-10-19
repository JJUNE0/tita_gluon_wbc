# tita_flash_sac_193248_068255_model_10000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "931de100525c66023cd7e84252ebef389700e12c12992616ea4e8e05884c2e0b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.18817257073821,
  "max_drift_m": 3.18817257073821,
  "radial_IAE_m_s": 97.19536463782237,
  "signed_longitudinal_delta_m": -3.1769476273727992,
  "tail_speed_mean_m_s": -0.05161064794456208,
  "tail_speed_rms_m_s": 0.05161266265268729,
  "tail_sensor_speed_mean_m_s": -0.05149881461946355,
  "tail_fk_speed_mean_m_s": -0.051497985612627854,
  "peak_tilt_rad": 0.034770655672792694,
  "peak_wheel_torque_nm": 0.5662797093391418,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.512236358015798
}
```
