# tita_flash_sac_115632_883848_model_20000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "517398e8dd4e04a0f4f1c405c08090f813bf638c6199a7e5c39261ff3d1ad6fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.976300017349176,
  "max_drift_m": 2.976300017349176,
  "radial_IAE_m_s": 94.17735518947543,
  "signed_longitudinal_delta_m": -2.9492156388202884,
  "tail_speed_mean_m_s": -0.042222234530134815,
  "tail_speed_rms_m_s": 0.0424332928063504,
  "tail_sensor_speed_mean_m_s": -0.04213035079359766,
  "tail_fk_speed_mean_m_s": -0.04212502699813115,
  "peak_tilt_rad": 0.13451619636299594,
  "peak_wheel_torque_nm": 0.2904578447341919,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.878987600037362
}
```
