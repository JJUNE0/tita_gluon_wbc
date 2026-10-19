# tita_flash_sac_115632_883848_model_20000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "a8cd85162e23328fc0277edc7ba2b89ec9dac7fc6717b99825ae4deb3b1d955b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017154883517796347,
  "max_drift_m": 0.086559451143449,
  "radial_IAE_m_s": 1.1228421219250966,
  "signed_longitudinal_delta_m": 0.006468480096589851,
  "tail_speed_mean_m_s": 9.907653553043285e-05,
  "tail_speed_rms_m_s": 9.909189080366966e-05,
  "tail_sensor_speed_mean_m_s": -0.00033610203860404413,
  "tail_fk_speed_mean_m_s": -2.043977161545468e-07,
  "peak_tilt_rad": 0.16454542544282247,
  "peak_wheel_torque_nm": 1.3543140888214111,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5095004139089654,
  "final_integral_m_s": 0.5095004139089654,
  "elapsed_wall_s": 10.277655119018164
}
```
