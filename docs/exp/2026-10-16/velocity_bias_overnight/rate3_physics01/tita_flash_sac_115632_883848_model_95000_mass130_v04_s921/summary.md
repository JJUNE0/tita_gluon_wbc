# tita_flash_sac_115632_883848_model_95000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "3720223327899b70b251ecb61cf2ad0e131b3bad1739f82fd85814e3613e47c4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.047828255379152966,
  "max_drift_m": 0.10651389486154805,
  "radial_IAE_m_s": 2.4340407540084774,
  "signed_longitudinal_delta_m": -0.04781570569567884,
  "tail_speed_mean_m_s": -0.0003614178383340201,
  "tail_speed_rms_m_s": 0.01373878110747978,
  "tail_sensor_speed_mean_m_s": -0.0009840622761987702,
  "tail_fk_speed_mean_m_s": 6.002429512065738e-05,
  "peak_tilt_rad": 0.16001989106353132,
  "peak_wheel_torque_nm": 4.3170270919799805,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.6057870773065932,
  "final_integral_m_s": -0.6057870773065932,
  "elapsed_wall_s": 12.756835751002654
}
```
