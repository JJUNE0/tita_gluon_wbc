# tita_flash_sac_115632_883848_model_30000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "initial_physics_sha256": "03f0d167fb161ab76c394797e7a9fc1890dfe31eb3baca0b038b0be4d1b25f2a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.051724324398237875,
  "max_drift_m": 0.1250444204553051,
  "radial_IAE_m_s": 3.237578166432967,
  "signed_longitudinal_delta_m": 0.051713676013939024,
  "tail_speed_mean_m_s": -5.955446497121929e-05,
  "tail_speed_rms_m_s": 5.9579908203230814e-05,
  "tail_sensor_speed_mean_m_s": -6.042912606643487e-05,
  "tail_fk_speed_mean_m_s": -5.907380664858219e-05,
  "peak_tilt_rad": 0.11731439769486829,
  "peak_wheel_torque_nm": 1.6676056385040283,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5396087019495746,
  "final_integral_m_s": 0.5397238524158664,
  "elapsed_wall_s": 4.429523864004295
}
```
