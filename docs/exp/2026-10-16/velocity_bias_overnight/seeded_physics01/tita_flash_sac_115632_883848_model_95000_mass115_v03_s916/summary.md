# tita_flash_sac_115632_883848_model_95000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "11c791aceec0cd17a4a22812ea264ef2312d183fc5ddf112aa52fc14b781203b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.059920101852044834,
  "max_drift_m": 0.10102929155233227,
  "radial_IAE_m_s": 3.645370332025109,
  "signed_longitudinal_delta_m": -0.0599201005544883,
  "tail_speed_mean_m_s": 1.8415669237479686e-05,
  "tail_speed_rms_m_s": 1.8438707843442276e-05,
  "tail_sensor_speed_mean_m_s": 1.8383484967693188e-05,
  "tail_fk_speed_mean_m_s": 1.832297619847719e-05,
  "peak_tilt_rad": 0.11358952989397553,
  "peak_wheel_torque_nm": 0.6012833714485168,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.587585452529793,
  "final_integral_m_s": -0.587585452529793,
  "elapsed_wall_s": 15.679514483024832
}
```
