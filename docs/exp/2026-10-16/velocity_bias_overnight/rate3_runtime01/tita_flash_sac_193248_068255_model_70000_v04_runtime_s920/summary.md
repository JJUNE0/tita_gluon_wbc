# tita_flash_sac_193248_068255_model_70000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "5899a87723511f621205c7346cbe2f74b72dc0bb97dfd58c4e278cb1c6d1719a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011460884219802524,
  "max_drift_m": 0.014111866268882467,
  "radial_IAE_m_s": 0.5614582952029563,
  "signed_longitudinal_delta_m": 0.011460877113936587,
  "tail_speed_mean_m_s": 6.784135010799257e-05,
  "tail_speed_rms_m_s": 6.830045067623873e-05,
  "tail_sensor_speed_mean_m_s": 6.782601945963018e-05,
  "tail_fk_speed_mean_m_s": 6.75680530826581e-05,
  "peak_tilt_rad": 0.075144759244548,
  "peak_wheel_torque_nm": 0.09495040029287338,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08510480988918441,
  "final_integral_m_s": 0.08510480988918441,
  "elapsed_wall_s": 12.153216535050888
}
```
