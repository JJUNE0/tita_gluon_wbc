# tita_flash_sac_115632_883848_model_40000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
    "estimator": "raw"
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "2d096d74441ac7489b4a7057fe8c5a0a39b29b0a8c177f7ef9b1afd89c62fd9c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022566014537066453,
  "max_drift_m": 0.04693479310817935,
  "radial_IAE_m_s": 1.4284066370400081,
  "signed_longitudinal_delta_m": 0.022550362302702277,
  "tail_speed_mean_m_s": 1.0571988121682682e-05,
  "tail_speed_rms_m_s": 0.007881278863042752,
  "tail_sensor_speed_mean_m_s": 0.0006860711751366049,
  "tail_fk_speed_mean_m_s": 5.9483657576744595e-05,
  "peak_tilt_rad": 0.11500564304957028,
  "peak_wheel_torque_nm": 1.4274866580963135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.39240930051156714,
  "final_integral_m_s": 0.260819425462941,
  "elapsed_wall_s": 4.336726895009633
}
```
