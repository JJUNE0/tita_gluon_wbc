# tita_flash_sac_193248_068255_model_100000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "31c86ebc81b01e453a846e4e75c555dbf7c2a5df9d0ffab8e046f4b42b2a34c6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.2451905608274325,
  "max_drift_m": 4.2451905608274325,
  "radial_IAE_m_s": 127.87309046337997,
  "signed_longitudinal_delta_m": 4.243595307734044,
  "tail_speed_mean_m_s": 0.06997167092553985,
  "tail_speed_rms_m_s": 0.06997202460152338,
  "tail_sensor_speed_mean_m_s": 0.06985170571344657,
  "tail_fk_speed_mean_m_s": 0.0698510882338847,
  "peak_tilt_rad": 0.05315011070525699,
  "peak_wheel_torque_nm": 0.37062376737594604,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.2791288899607025
}
```
