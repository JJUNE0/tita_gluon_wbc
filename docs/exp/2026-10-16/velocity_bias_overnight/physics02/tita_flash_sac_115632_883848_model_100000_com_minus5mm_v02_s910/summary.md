# tita_flash_sac_115632_883848_model_100000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "bf6e040e34a6d8b811ddbfbc25fc3c63f4e8ce579469f58079595e07140fea17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0464139137694402,
  "max_drift_m": 0.056251156019887914,
  "radial_IAE_m_s": 2.6935905661468604,
  "signed_longitudinal_delta_m": 0.046413612031756694,
  "tail_speed_mean_m_s": 4.33267488584148e-05,
  "tail_speed_rms_m_s": 4.33323326482263e-05,
  "tail_sensor_speed_mean_m_s": 4.310268550463038e-05,
  "tail_fk_speed_mean_m_s": 4.313080144859475e-05,
  "peak_tilt_rad": 0.08337256855497843,
  "peak_wheel_torque_nm": 0.43846091628074646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4687694724768032,
  "final_integral_m_s": 0.46868065080080107,
  "elapsed_wall_s": 11.511174839979503
}
```
