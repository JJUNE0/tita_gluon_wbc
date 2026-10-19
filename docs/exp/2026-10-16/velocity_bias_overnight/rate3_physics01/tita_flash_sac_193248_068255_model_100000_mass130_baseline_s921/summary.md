# tita_flash_sac_193248_068255_model_100000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "73ae4d1ac6d04150218c27581c7eaa63c27db8908906d0322d46cdae399038de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.489325889728423,
  "max_drift_m": 9.489325889728423,
  "radial_IAE_m_s": 285.71583399913936,
  "signed_longitudinal_delta_m": -9.482096545543959,
  "tail_speed_mean_m_s": -0.15694367590998637,
  "tail_speed_rms_m_s": 0.15735089345224954,
  "tail_sensor_speed_mean_m_s": -0.15685730075708204,
  "tail_fk_speed_mean_m_s": -0.15644534098342391,
  "peak_tilt_rad": 0.06756435632261781,
  "peak_wheel_torque_nm": 3.9069600105285645,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.792386012035422
}
```
