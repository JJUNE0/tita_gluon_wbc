# tita_flash_sac_115632_883848_model_60000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "82b38840161f009f085cc5bc7b97143f94203aff26571f5474187b78a331f37f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0013465306200444868,
  "max_drift_m": 0.08245053650141368,
  "radial_IAE_m_s": 0.23299718115022183,
  "signed_longitudinal_delta_m": 0.0012385725877350486,
  "tail_speed_mean_m_s": -2.456438857822121e-05,
  "tail_speed_rms_m_s": 2.5465838945794438e-05,
  "tail_sensor_speed_mean_m_s": -2.4588339752496393e-05,
  "tail_fk_speed_mean_m_s": -2.2484294703363143e-05,
  "peak_tilt_rad": 0.09504722527339116,
  "peak_wheel_torque_nm": 1.563069224357605,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047510417016829704,
  "final_integral_m_s": 0.047510417016829704,
  "elapsed_wall_s": 13.284497739979997
}
```
