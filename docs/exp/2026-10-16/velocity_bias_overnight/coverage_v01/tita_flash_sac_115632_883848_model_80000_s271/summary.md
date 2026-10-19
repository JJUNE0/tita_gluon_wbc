# tita_flash_sac_115632_883848_model_80000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "7615c78b917077191c5976ee5ca765151e46a2561d3d77c8954c061526efe36d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0808875011256649,
  "max_drift_m": 0.10987308737253333,
  "radial_IAE_m_s": 4.754761406733283,
  "signed_longitudinal_delta_m": 0.08085923607101157,
  "tail_speed_mean_m_s": 5.4889303958969433e-05,
  "tail_speed_rms_m_s": 5.4933530850445806e-05,
  "tail_sensor_speed_mean_m_s": 5.4533726176041995e-05,
  "tail_fk_speed_mean_m_s": 5.485113495909405e-05,
  "peak_tilt_rad": 0.08579146193334819,
  "peak_wheel_torque_nm": 0.9970595836639404,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8336524478649064,
  "final_integral_m_s": 0.833540405085087,
  "elapsed_wall_s": 4.448429965006653
}
```
