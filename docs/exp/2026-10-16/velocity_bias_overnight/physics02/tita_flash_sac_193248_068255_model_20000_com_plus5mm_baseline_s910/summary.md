# tita_flash_sac_193248_068255_model_20000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "03224a388386a65d37250023bc8fe57eae3bc033876bc3a05bbe636d62a2d038",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.946901600002242,
  "max_drift_m": 13.946901600002242,
  "radial_IAE_m_s": 418.2162948590345,
  "signed_longitudinal_delta_m": 13.924675815608122,
  "tail_speed_mean_m_s": 0.23377394675743107,
  "tail_speed_rms_m_s": 0.23377394676686153,
  "tail_sensor_speed_mean_m_s": 0.23326946186788408,
  "tail_fk_speed_mean_m_s": 0.23326111021766557,
  "peak_tilt_rad": 0.16602832531889034,
  "peak_wheel_torque_nm": 0.3190157413482666,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.243670141033363
}
```
