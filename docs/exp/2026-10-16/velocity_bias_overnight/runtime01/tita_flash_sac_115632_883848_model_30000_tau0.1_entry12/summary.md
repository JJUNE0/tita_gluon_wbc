# tita_flash_sac_115632_883848_model_30000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "0177e6585c3fa2963446837a4ea0c03bea55d42ff167c1b8f9a552dfc680ada0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.053481546812709654,
  "max_drift_m": 0.1171609724199012,
  "radial_IAE_m_s": 3.2406449433622733,
  "signed_longitudinal_delta_m": 0.05346714868553615,
  "tail_speed_mean_m_s": -1.3680612130600483e-05,
  "tail_speed_rms_m_s": 1.948061231009889e-05,
  "tail_sensor_speed_mean_m_s": -1.484843574758838e-05,
  "tail_fk_speed_mean_m_s": -1.3219859975640021e-05,
  "peak_tilt_rad": 0.12695744038819923,
  "peak_wheel_torque_nm": 1.1175204515457153,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5619797308262321,
  "final_integral_m_s": 0.5620720736050794,
  "elapsed_wall_s": 6.016339547000825
}
```
