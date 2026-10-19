# tita_flash_sac_193248_068255_model_10000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "e31e4f28a0e7407b6fad2c3bf501657f1185f2ccee9e7d1a9f03458323901aac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5554297181012907,
  "max_drift_m": 0.5554297181012907,
  "radial_IAE_m_s": 19.252873796041563,
  "signed_longitudinal_delta_m": 0.5118215811026977,
  "tail_speed_mean_m_s": 0.006991620039780564,
  "tail_speed_rms_m_s": 0.007162107459466853,
  "tail_sensor_speed_mean_m_s": 0.006921909732174218,
  "tail_fk_speed_mean_m_s": 0.006982319940120135,
  "peak_tilt_rad": 0.02788234628560282,
  "peak_wheel_torque_nm": 0.886975109577179,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.374783162027597
}
```
