# tita_flash_sac_193248_068255_model_5000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "38149c1c9f13477c1be3356eced1c9b0f58c0eeeae3321623fb8de88c051316d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20210415818940783,
  "max_drift_m": 0.20383780158395687,
  "radial_IAE_m_s": 11.560999875061922,
  "signed_longitudinal_delta_m": -0.20205824530574076,
  "tail_speed_mean_m_s": 3.694437380965459e-05,
  "tail_speed_rms_m_s": 3.697273260105372e-05,
  "tail_sensor_speed_mean_m_s": 3.1686516669449514e-05,
  "tail_fk_speed_mean_m_s": 2.5882867431742318e-05,
  "peak_tilt_rad": 0.07519943264080431,
  "peak_wheel_torque_nm": 0.9056716561317444,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0138888183738533,
  "final_integral_m_s": -1.0138888183738533,
  "elapsed_wall_s": 13.262278570968192
}
```
