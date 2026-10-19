# p002_tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 2.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 2.0
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "3a4ba1ca68189c8896b3491841cd28abf61e8aa5305f036f14ac64ec8a9f372d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009952759285510126,
  "max_drift_m": 0.08303702034382614,
  "radial_IAE_m_s": 0.6049649212300885,
  "signed_longitudinal_delta_m": -0.009946675154634644,
  "tail_speed_mean_m_s": -9.190792272104225e-05,
  "tail_speed_rms_m_s": 9.203041260278925e-05,
  "tail_sensor_speed_mean_m_s": -9.131676110344598e-05,
  "tail_fk_speed_mean_m_s": -8.926012958943776e-05,
  "peak_tilt_rad": 0.1138490780028476,
  "peak_wheel_torque_nm": 2.0372250080108643,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3505985723836956,
  "final_integral_m_s": -0.3505985723836956,
  "elapsed_wall_s": 5.31298801099183
}
```
