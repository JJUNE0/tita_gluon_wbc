# tita_flash_sac_115632_883848_model_60000_com_minus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_minus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "fe0ce59e2ecfc91c47bba60dcfeecec831868c751be20b59d55275193d9057cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0024051049009431885,
  "max_drift_m": 0.0024051049009431885,
  "radial_IAE_m_s": 0.41425948200167584,
  "signed_longitudinal_delta_m": 0.0006854504921518797,
  "tail_speed_mean_m_s": -9.393337824464718e-08,
  "tail_speed_rms_m_s": 1.2275345210536202e-06,
  "tail_sensor_speed_mean_m_s": -8.878299619238289e-07,
  "tail_fk_speed_mean_m_s": 1.4314741191937662e-06,
  "peak_tilt_rad": 0.0683956491548754,
  "peak_wheel_torque_nm": 0.1536809653043747,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.017752375838255938,
  "final_integral_m_s": 0.017751041627954524,
  "elapsed_wall_s": 43.99934406502871
}
```
