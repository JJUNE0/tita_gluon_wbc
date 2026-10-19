# tita_flash_sac_115632_883848_model_80000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "ec06fd0dd72efbeaa0a3d6af52b4f862bf72d214589df6a9a493df6a5d0a6c77",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.130379747476143,
  "max_drift_m": 0.13868251502474946,
  "radial_IAE_m_s": 7.498901877987416,
  "signed_longitudinal_delta_m": 0.1303435240857281,
  "tail_speed_mean_m_s": 0.00012935092475738774,
  "tail_speed_rms_m_s": 0.0001353763676613977,
  "tail_sensor_speed_mean_m_s": 0.00012896388550289836,
  "tail_fk_speed_mean_m_s": 0.00012925545472078763,
  "peak_tilt_rad": 0.08429462001351729,
  "peak_wheel_torque_nm": 0.7057921886444092,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8192603897637544,
  "final_integral_m_s": 0.8192603897637544,
  "elapsed_wall_s": 13.035566106031183
}
```
