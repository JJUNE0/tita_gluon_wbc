# tita_flash_sac_193248_068255_model_100000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "2904910b1c795db9244dbe3772efd6a5742088a6505ecf3e2e705fb1c17f8552",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04718124953942959,
  "max_drift_m": 0.05471709237809091,
  "radial_IAE_m_s": 2.6029088716054885,
  "signed_longitudinal_delta_m": -0.047181235380745874,
  "tail_speed_mean_m_s": -0.00010904488437683754,
  "tail_speed_rms_m_s": 0.0030046252235139044,
  "tail_sensor_speed_mean_m_s": 0.0007689245530412234,
  "tail_fk_speed_mean_m_s": -3.06483518249328e-05,
  "peak_tilt_rad": 0.08658334497231435,
  "peak_wheel_torque_nm": 2.050427198410034,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2666669609608223,
  "final_integral_m_s": -0.2666669609608223,
  "elapsed_wall_s": 8.427782749000471
}
```
