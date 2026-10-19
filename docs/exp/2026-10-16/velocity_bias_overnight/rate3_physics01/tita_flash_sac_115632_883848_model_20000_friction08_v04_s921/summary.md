# tita_flash_sac_115632_883848_model_20000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "251658f19e4f9fda30805d75c2719d1a46a22f649fe2e1aa56899e8a6b1ee9f7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02907189313818266,
  "max_drift_m": 0.095216783319973,
  "radial_IAE_m_s": 1.903978565552349,
  "signed_longitudinal_delta_m": -0.02822713255899445,
  "tail_speed_mean_m_s": -0.00012174332316398909,
  "tail_speed_rms_m_s": 0.0015277725691991194,
  "tail_sensor_speed_mean_m_s": -9.723414894860345e-05,
  "tail_fk_speed_mean_m_s": -8.027905243163681e-05,
  "peak_tilt_rad": 0.15218652686561795,
  "peak_wheel_torque_nm": 0.9696270823478699,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27079790259520486,
  "final_integral_m_s": 0.27079790259520486,
  "elapsed_wall_s": 10.205553735955618
}
```
