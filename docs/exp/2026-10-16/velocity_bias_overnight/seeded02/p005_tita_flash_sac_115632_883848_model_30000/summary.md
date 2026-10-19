# p005_tita_flash_sac_115632_883848_model_30000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p005_tita_flash_sac_115632_883848_model_30000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
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
  "final_drift_m": 0.07403234924310868,
  "max_drift_m": 0.14886301362645055,
  "radial_IAE_m_s": 4.453969628592507,
  "signed_longitudinal_delta_m": -0.07403185278593927,
  "tail_speed_mean_m_s": -6.280169114059957e-05,
  "tail_speed_rms_m_s": 7.711471537782066e-05,
  "tail_sensor_speed_mean_m_s": -6.378460320532773e-05,
  "tail_fk_speed_mean_m_s": -6.22627228635402e-05,
  "peak_tilt_rad": 0.12682070967757864,
  "peak_wheel_torque_nm": 1.0665392875671387,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5594873966892574,
  "final_integral_m_s": 0.5594873966892574,
  "elapsed_wall_s": 4.738742520974483
}
```
