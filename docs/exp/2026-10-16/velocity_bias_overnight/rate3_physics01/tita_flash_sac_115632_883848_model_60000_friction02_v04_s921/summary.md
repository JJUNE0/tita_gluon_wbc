# tita_flash_sac_115632_883848_model_60000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "initial_physics_sha256": "6ed5d01679f8c763956f29d0207cfec11980da29afb8fa196f3cdb9fff09bee6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004216097250565953,
  "max_drift_m": 0.007684853342400316,
  "radial_IAE_m_s": 0.2092384210177486,
  "signed_longitudinal_delta_m": -0.0041883845240713044,
  "tail_speed_mean_m_s": 5.77330246804551e-07,
  "tail_speed_rms_m_s": 5.893826237112446e-07,
  "tail_sensor_speed_mean_m_s": -3.478134417088113e-05,
  "tail_fk_speed_mean_m_s": -1.5839987181321637e-07,
  "peak_tilt_rad": 0.06149666157654776,
  "peak_wheel_torque_nm": 0.17789071798324585,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04234299627640497,
  "final_integral_m_s": 0.04234299627640497,
  "elapsed_wall_s": 8.374392618017737
}
```
