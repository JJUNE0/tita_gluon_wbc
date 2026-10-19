# tita_flash_sac_115632_883848_model_30000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "initial_physics_sha256": "1dadf31fa54d586d3b20a7abda35522f0fa98abdaecb7a2abb97e8ee401c418d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020617262202864826,
  "max_drift_m": 0.10231065964088423,
  "radial_IAE_m_s": 1.3533396329733773,
  "signed_longitudinal_delta_m": -0.02059909141322157,
  "tail_speed_mean_m_s": -3.501018548516494e-05,
  "tail_speed_rms_m_s": 4.9923079958701955e-05,
  "tail_sensor_speed_mean_m_s": -3.6116619736238325e-05,
  "tail_fk_speed_mean_m_s": -3.4501009133450805e-05,
  "peak_tilt_rad": 0.12694170412969785,
  "peak_wheel_torque_nm": 1.4238791465759277,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5619316009446175,
  "final_integral_m_s": 0.5619316009446175,
  "elapsed_wall_s": 12.600797737017274
}
```
