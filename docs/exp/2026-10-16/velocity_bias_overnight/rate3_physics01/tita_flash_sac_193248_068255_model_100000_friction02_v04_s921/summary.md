# tita_flash_sac_193248_068255_model_100000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "31c86ebc81b01e453a846e4e75c555dbf7c2a5df9d0ffab8e046f4b42b2a34c6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025308580580363966,
  "max_drift_m": 0.043687783835721396,
  "radial_IAE_m_s": 1.4992532625770725,
  "signed_longitudinal_delta_m": 0.025304396868442793,
  "tail_speed_mean_m_s": 2.3270033727966366e-05,
  "tail_speed_rms_m_s": 2.3295309894856243e-05,
  "tail_sensor_speed_mean_m_s": 2.322726616143737e-05,
  "tail_fk_speed_mean_m_s": 2.3170449082881166e-05,
  "peak_tilt_rad": 0.052478267298101455,
  "peak_wheel_torque_nm": 0.2734009325504303,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2694583367053967,
  "final_integral_m_s": 0.2694583367053967,
  "elapsed_wall_s": 7.597203433979303
}
```
