# tita_flash_sac_193248_068255_model_5000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "eb73435498c4ebbcd879e2eeaffe825d89bfae84c3f5e0751006370a044a2fa3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.21048455744925745,
  "max_drift_m": 0.21172093814436518,
  "radial_IAE_m_s": 12.139744210029178,
  "signed_longitudinal_delta_m": -0.21042807704929345,
  "tail_speed_mean_m_s": 2.6153896829089773e-05,
  "tail_speed_rms_m_s": 2.6155649125541723e-05,
  "tail_sensor_speed_mean_m_s": 8.956960334998391e-06,
  "tail_fk_speed_mean_m_s": -1.3945332448496692e-06,
  "peak_tilt_rad": 0.09385920424504457,
  "peak_wheel_torque_nm": 1.8560874462127686,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.116705305309284,
  "final_integral_m_s": -1.116705305309284,
  "elapsed_wall_s": 12.074893898970913
}
```
