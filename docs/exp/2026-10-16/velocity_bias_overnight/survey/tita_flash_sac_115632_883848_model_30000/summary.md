# tita_flash_sac_115632_883848_model_30000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "ad05cc1b5a3e78ca6f14665efddb59d2aded95dcf09d82ff72481e7fa332c125",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.973685118382567,
  "max_drift_m": 13.973685118382567,
  "radial_IAE_m_s": 422.2092444860071,
  "signed_longitudinal_delta_m": 13.90715539394621,
  "tail_speed_mean_m_s": 0.23113837899599848,
  "tail_speed_rms_m_s": 0.2311384055672158,
  "tail_sensor_speed_mean_m_s": 0.2306378063748553,
  "tail_fk_speed_mean_m_s": 0.23063608910372463,
  "peak_tilt_rad": 0.11731447962082497,
  "peak_wheel_torque_nm": 0.01866936683654785,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.411400509008672
}
```
