# tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "afb34808bdd5f78eee5334c8c02461d8a5a5636dff473cf20d3033a98906a294",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2416450198154213,
  "max_drift_m": 0.2416450198154213,
  "radial_IAE_m_s": 5.6232570781996785,
  "signed_longitudinal_delta_m": 0.23566627534079404,
  "tail_speed_mean_m_s": 0.0059760254299888295,
  "tail_speed_rms_m_s": 0.005979633510369154,
  "tail_sensor_speed_mean_m_s": 0.005984647046677905,
  "tail_fk_speed_mean_m_s": 0.005991859072987217,
  "peak_tilt_rad": 0.04074191550624362,
  "peak_wheel_torque_nm": 3.8651533126831055,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.963209819979966
}
```
