# tita_flash_sac_115632_883848_model_60000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "initial_physics_sha256": "47355ae18415082697d8142ceba3f5f18c722d1ea42d99c19b5b69c24f80b81f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0030174066935672317,
  "max_drift_m": 0.0623104653656383,
  "radial_IAE_m_s": 0.34873003347925635,
  "signed_longitudinal_delta_m": -0.002981729704398211,
  "tail_speed_mean_m_s": 1.3546132309793122e-06,
  "tail_speed_rms_m_s": 0.011644098345720793,
  "tail_sensor_speed_mean_m_s": -0.0002631232085308406,
  "tail_fk_speed_mean_m_s": 9.012034840507649e-05,
  "peak_tilt_rad": 0.18512619454779555,
  "peak_wheel_torque_nm": 5.31479549407959,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4144564880651948,
  "final_integral_m_s": -0.4144564880651948,
  "elapsed_wall_s": 7.38615471002413
}
```
