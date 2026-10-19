# tita_flash_sac_115632_883848_model_30000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "initial_physics_sha256": "506fdb554add296c9312f02d131fa8cfcb1b5c1f3a9ac64f7ebe12266176398b",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.05218923593104833,
  "max_drift_m": 0.10237008633984962,
  "radial_IAE_m_s": 10.15548741275594,
  "signed_longitudinal_delta_m": -0.05215089522573165,
  "tail_speed_mean_m_s": -0.00013875333819615414,
  "tail_speed_rms_m_s": 0.0001388563355410074,
  "tail_sensor_speed_mean_m_s": -0.00013882736624684186,
  "tail_fk_speed_mean_m_s": -0.00013824556193220598,
  "peak_tilt_rad": 0.1271062016011857,
  "peak_wheel_torque_nm": 1.4239344596862793,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.43600319621449063,
  "final_integral_m_s": 0.43600319621449063,
  "elapsed_wall_s": 58.11608512297971
}
```
