# tita_flash_sac_115632_883848_model_95000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "initial_physics_sha256": "89159ca90fa9f99546805a42ac7da1a297e97bf7ce785af8c3aaefc0ef4910ba",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.10864749427719125,
  "max_drift_m": 0.10864749427719125,
  "radial_IAE_m_s": 17.84874776747543,
  "signed_longitudinal_delta_m": 0.10713083206552582,
  "tail_speed_mean_m_s": 0.0002877300300611078,
  "tail_speed_rms_m_s": 0.0002877407469783795,
  "tail_sensor_speed_mean_m_s": 0.00028646255986124306,
  "tail_fk_speed_mean_m_s": 0.000287343054706914,
  "peak_tilt_rad": 0.06301957389233626,
  "peak_wheel_torque_nm": 0.18516094982624054,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4056474002766714,
  "final_integral_m_s": 0.4056474002766714,
  "elapsed_wall_s": 44.23110345902387
}
```
