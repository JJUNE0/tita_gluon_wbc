# tita_flash_sac_193248_068255_model_5000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "5b72cdc663a8f0b30c38d6d96cc7eb00379427f44a92f7d5e1ca5df0cf2f54c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019974694599307223,
  "max_drift_m": 0.08999596221613644,
  "radial_IAE_m_s": 2.4332132501436483,
  "signed_longitudinal_delta_m": -0.019974535731327136,
  "tail_speed_mean_m_s": -0.0003204638813303422,
  "tail_speed_rms_m_s": 0.031124884177393362,
  "tail_sensor_speed_mean_m_s": -0.0005574081663359789,
  "tail_fk_speed_mean_m_s": -0.00010738234013570223,
  "peak_tilt_rad": 0.12936960689227295,
  "peak_wheel_torque_nm": 3.161315679550171,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03154570308762817,
  "final_integral_m_s": -0.14894303177116383,
  "elapsed_wall_s": 4.48861240799306
}
```
