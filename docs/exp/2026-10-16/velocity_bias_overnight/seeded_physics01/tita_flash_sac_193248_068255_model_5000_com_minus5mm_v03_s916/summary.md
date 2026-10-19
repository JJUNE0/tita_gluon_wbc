# tita_flash_sac_193248_068255_model_5000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "d291f87862ff51d705986891dd450a4bbae317e4080d3ff98eda72bdb9d1daec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2058807346961631,
  "max_drift_m": 0.20798640601717733,
  "radial_IAE_m_s": 11.842030187007659,
  "signed_longitudinal_delta_m": -0.20585235380833122,
  "tail_speed_mean_m_s": 3.4622985504618275e-05,
  "tail_speed_rms_m_s": 3.471944753105508e-05,
  "tail_sensor_speed_mean_m_s": 2.824829169452879e-05,
  "tail_fk_speed_mean_m_s": 2.2502167027638417e-05,
  "peak_tilt_rad": 0.07359006115482991,
  "peak_wheel_torque_nm": 0.7520232200622559,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0493709821754504,
  "final_integral_m_s": -1.0493709821754504,
  "elapsed_wall_s": 12.837777451029979
}
```
