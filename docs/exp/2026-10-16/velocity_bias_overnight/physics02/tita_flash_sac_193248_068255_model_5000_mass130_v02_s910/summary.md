# tita_flash_sac_193248_068255_model_5000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "c22ab1310630f8725517f84096431383f28c65f58a40a5b569aa504715a1d06d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12293308185882881,
  "max_drift_m": 0.12463512914580507,
  "radial_IAE_m_s": 7.340039386742674,
  "signed_longitudinal_delta_m": -0.12293248376069488,
  "tail_speed_mean_m_s": 2.8763991075705897e-05,
  "tail_speed_rms_m_s": 2.8814663929420267e-05,
  "tail_sensor_speed_mean_m_s": 1.4079684260580065e-05,
  "tail_fk_speed_mean_m_s": 8.24597577241343e-06,
  "peak_tilt_rad": 0.1482825221466011,
  "peak_wheel_torque_nm": 2.952815532684326,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.2653703721746568,
  "final_integral_m_s": -1.2653878563464402,
  "elapsed_wall_s": 11.364195838978048
}
```
