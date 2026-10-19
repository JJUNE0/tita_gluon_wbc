# tita_flash_sac_193248_068255_model_5000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "2830577c8f6653f3b658c73f6bafc708105060f629126d28416261e949a786c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09648013018664306,
  "max_drift_m": 0.09854491699773227,
  "radial_IAE_m_s": 5.69699110137544,
  "signed_longitudinal_delta_m": -0.09643607510042747,
  "tail_speed_mean_m_s": 3.860286404751137e-05,
  "tail_speed_rms_m_s": 3.8936896518014904e-05,
  "tail_sensor_speed_mean_m_s": 3.123775850732179e-05,
  "tail_fk_speed_mean_m_s": 2.438681919548738e-05,
  "peak_tilt_rad": 0.07562808644161079,
  "peak_wheel_torque_nm": 1.2023876905441284,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.983213683049829,
  "final_integral_m_s": -0.9832487282149713,
  "elapsed_wall_s": 11.335674105968792
}
```
