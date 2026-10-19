# tita_flash_sac_193248_068255_model_10000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "6c264991f9fb64e8f37df8fce9a613f16e9d83597e9d20c2938526d1fc31b4ad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07215427576243513,
  "max_drift_m": 0.0733405664036748,
  "radial_IAE_m_s": 2.8374524132195247,
  "signed_longitudinal_delta_m": -0.022538150958548674,
  "tail_speed_mean_m_s": -0.0007705419253668822,
  "tail_speed_rms_m_s": 0.0008163775574782052,
  "tail_sensor_speed_mean_m_s": -0.0009390048883748273,
  "tail_fk_speed_mean_m_s": -0.0008293040397298108,
  "peak_tilt_rad": 0.05699748329997689,
  "peak_wheel_torque_nm": 0.8193529844284058,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.40292927630994607,
  "final_integral_m_s": -0.40292927630994607,
  "elapsed_wall_s": 12.58805859304266
}
```
