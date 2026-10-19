# tita_flash_sac_115632_883848_model_75000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "72e93bbcae37721aa9147da47559d7a551983a03b559309dcb77361f126c6c5b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03423884245250974,
  "max_drift_m": 0.09908682937407998,
  "radial_IAE_m_s": 2.1016359226984376,
  "signed_longitudinal_delta_m": 0.03423372307644869,
  "tail_speed_mean_m_s": 1.984549284472818e-05,
  "tail_speed_rms_m_s": 1.9850638422887026e-05,
  "tail_sensor_speed_mean_m_s": 1.9740702452464727e-05,
  "tail_fk_speed_mean_m_s": 1.9880350786973033e-05,
  "peak_tilt_rad": 0.18474408334290215,
  "peak_wheel_torque_nm": 1.671400785446167,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4990926621934174,
  "final_integral_m_s": -0.4990926621934174,
  "elapsed_wall_s": 10.213204249041155
}
```
