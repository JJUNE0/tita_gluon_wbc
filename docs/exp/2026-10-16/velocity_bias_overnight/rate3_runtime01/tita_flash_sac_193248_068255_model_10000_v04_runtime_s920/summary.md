# tita_flash_sac_193248_068255_model_10000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "d1d4c02cdf9ad23bd98c306706650405624e29abb2671e52a9eb85117b98a639",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020032412972290598,
  "max_drift_m": 0.020032412972290598,
  "radial_IAE_m_s": 0.8466932146573188,
  "signed_longitudinal_delta_m": 0.019798298939706947,
  "tail_speed_mean_m_s": 0.00017068251552705666,
  "tail_speed_rms_m_s": 0.0001707709393945327,
  "tail_sensor_speed_mean_m_s": 0.00018406605810854972,
  "tail_fk_speed_mean_m_s": 0.00019077236133283645,
  "peak_tilt_rad": 0.02474238138640599,
  "peak_wheel_torque_nm": 0.8896925449371338,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11180881312610681,
  "final_integral_m_s": 0.11180881312610681,
  "elapsed_wall_s": 12.928180096030701
}
```
