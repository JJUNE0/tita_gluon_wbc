# tita_flash_sac_115632_883848_model_90000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.038216778983140735,
  "max_drift_m": 0.052888610232881744,
  "radial_IAE_m_s": 2.224763643867078,
  "signed_longitudinal_delta_m": 0.03821575498092826,
  "tail_speed_mean_m_s": 3.4960471243314353e-05,
  "tail_speed_rms_m_s": 3.560844036816043e-05,
  "tail_sensor_speed_mean_m_s": 3.459950375599941e-05,
  "tail_fk_speed_mean_m_s": 3.577080985180227e-05,
  "peak_tilt_rad": 0.06904603056173708,
  "peak_wheel_torque_nm": 0.34441301226615906,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.39012483819100735,
  "final_integral_m_s": 0.39003316310815345,
  "elapsed_wall_s": 5.756899927044287
}
```
