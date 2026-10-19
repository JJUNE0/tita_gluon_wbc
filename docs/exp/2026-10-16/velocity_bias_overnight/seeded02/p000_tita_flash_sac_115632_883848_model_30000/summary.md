# p000_tita_flash_sac_115632_883848_model_30000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p000_tita_flash_sac_115632_883848_model_30000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "f07a29c93293b5218116b72710e08be8c6207cc8caef81eb69981149663b2c79",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026624135846323047,
  "max_drift_m": 0.11576262785479736,
  "radial_IAE_m_s": 1.71005192144,
  "signed_longitudinal_delta_m": -0.02661450876982924,
  "tail_speed_mean_m_s": -5.0396468812498543e-05,
  "tail_speed_rms_m_s": 7.070794499056089e-05,
  "tail_sensor_speed_mean_m_s": -5.148497967211769e-05,
  "tail_fk_speed_mean_m_s": -4.985511254423033e-05,
  "peak_tilt_rad": 0.12682768140274026,
  "peak_wheel_torque_nm": 0.8573290705680847,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5616773846122555,
  "final_integral_m_s": 0.5616773846122555,
  "elapsed_wall_s": 5.0446551000350155
}
```
