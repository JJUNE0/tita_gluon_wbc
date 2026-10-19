# tita_flash_sac_115632_883848_model_30000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "ca9555395ca1e710f0a8f711e08568112af6a86e2a8ee68199529dba7d8901ad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.032301509293312415,
  "max_drift_m": 0.044088995835432805,
  "radial_IAE_m_s": 1.743673265983337,
  "signed_longitudinal_delta_m": -0.03230129054803598,
  "tail_speed_mean_m_s": -9.21823894468723e-05,
  "tail_speed_rms_m_s": 9.267088939220845e-05,
  "tail_sensor_speed_mean_m_s": -9.221499807455744e-05,
  "tail_fk_speed_mean_m_s": -9.188719428404351e-05,
  "peak_tilt_rad": 0.08787159883866136,
  "peak_wheel_torque_nm": 0.41482406854629517,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.012594234199345968,
  "final_integral_m_s": -0.012594234199345968,
  "elapsed_wall_s": 10.634780615975615
}
```
