# tita_flash_sac_115632_883848_model_85000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "c3ad821a18e209e5b83758c583a3f1f4204a0cd4faaa454283a68eb42eaf29db",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009966498315085464,
  "max_drift_m": 0.017661046542336935,
  "radial_IAE_m_s": 0.6099529312146417,
  "signed_longitudinal_delta_m": -0.00996111247020648,
  "tail_speed_mean_m_s": 3.767127115047902e-06,
  "tail_speed_rms_m_s": 3.76860330319932e-06,
  "tail_sensor_speed_mean_m_s": 3.795917198187522e-06,
  "tail_fk_speed_mean_m_s": 3.704565763403654e-06,
  "peak_tilt_rad": 0.07488453835241149,
  "peak_wheel_torque_nm": 0.30725592374801636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.10634182740094082,
  "final_integral_m_s": -0.10634916363085521,
  "elapsed_wall_s": 17.802758756035473
}
```
