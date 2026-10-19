# tita_flash_sac_193248_068255_model_10000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "ddc57f50556c60fd9ca922d9c8b6a32feaf72c150b29f2ac5b58de70a2abebb9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05289853838963506,
  "max_drift_m": 0.05289853838963506,
  "radial_IAE_m_s": 2.7516131387067557,
  "signed_longitudinal_delta_m": 0.052831679051483935,
  "tail_speed_mean_m_s": 0.00015010041122205035,
  "tail_speed_rms_m_s": 0.00015018723046942515,
  "tail_sensor_speed_mean_m_s": 0.00015549456748055606,
  "tail_fk_speed_mean_m_s": 0.000160863193438627,
  "peak_tilt_rad": 0.02876652935061652,
  "peak_wheel_torque_nm": 0.8560863137245178,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2876862223737602,
  "final_integral_m_s": 0.2876862223737602,
  "elapsed_wall_s": 10.478303888987284
}
```
