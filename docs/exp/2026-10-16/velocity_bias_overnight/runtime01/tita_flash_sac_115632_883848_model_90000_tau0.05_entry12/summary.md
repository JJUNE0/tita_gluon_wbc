# tita_flash_sac_115632_883848_model_90000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "3e68a8d06f8a123b74498590ef73b506307b43afcb037c9143a919edafd0f49b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03821081824832547,
  "max_drift_m": 0.04594562850480787,
  "radial_IAE_m_s": 2.2197139881286807,
  "signed_longitudinal_delta_m": 0.0382096658685323,
  "tail_speed_mean_m_s": 3.477340620327818e-05,
  "tail_speed_rms_m_s": 3.5383048541549954e-05,
  "tail_sensor_speed_mean_m_s": 3.4414436207346685e-05,
  "tail_fk_speed_mean_m_s": 3.558429809496465e-05,
  "peak_tilt_rad": 0.06904603056173708,
  "peak_wheel_torque_nm": 0.5573344826698303,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.39008004653834044,
  "final_integral_m_s": 0.38998838723623386,
  "elapsed_wall_s": 5.807650883041788
}
```
