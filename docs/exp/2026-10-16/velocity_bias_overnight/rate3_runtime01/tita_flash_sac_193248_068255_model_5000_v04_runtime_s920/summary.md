# tita_flash_sac_193248_068255_model_5000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "069ffc85a50d623a2d81493cab7051c8c7c679bed68865779ac19e967d63f922",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20178639862656628,
  "max_drift_m": 0.2034274601172052,
  "radial_IAE_m_s": 11.545016762754832,
  "signed_longitudinal_delta_m": -0.2017420851645622,
  "tail_speed_mean_m_s": 3.7606646581004374e-05,
  "tail_speed_rms_m_s": 3.762869494448693e-05,
  "tail_sensor_speed_mean_m_s": 3.272320714598152e-05,
  "tail_fk_speed_mean_m_s": 2.703657821149682e-05,
  "peak_tilt_rad": 0.0752208695299319,
  "peak_wheel_torque_nm": 0.8991221189498901,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0133589689479932,
  "final_integral_m_s": -1.0133589689479932,
  "elapsed_wall_s": 12.824197791982442
}
```
