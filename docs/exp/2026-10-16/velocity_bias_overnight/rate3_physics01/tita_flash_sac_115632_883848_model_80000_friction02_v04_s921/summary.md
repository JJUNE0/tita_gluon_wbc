# tita_flash_sac_115632_883848_model_80000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "f13a88290e66d84dae03c60f55834175a759fb0191697aeb89a1872afa5e5353",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1366704965914639,
  "max_drift_m": 0.14751085422083854,
  "radial_IAE_m_s": 8.45366603228395,
  "signed_longitudinal_delta_m": 0.13655640732735574,
  "tail_speed_mean_m_s": -7.050538664945654e-05,
  "tail_speed_rms_m_s": 7.050932379312497e-05,
  "tail_sensor_speed_mean_m_s": 0.00016138437878327583,
  "tail_fk_speed_mean_m_s": 3.1283644928889917e-08,
  "peak_tilt_rad": 0.08004357618784597,
  "peak_wheel_torque_nm": 0.6242775917053223,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8627934823691465,
  "final_integral_m_s": 0.8627934823691465,
  "elapsed_wall_s": 8.57284505397547
}
```
