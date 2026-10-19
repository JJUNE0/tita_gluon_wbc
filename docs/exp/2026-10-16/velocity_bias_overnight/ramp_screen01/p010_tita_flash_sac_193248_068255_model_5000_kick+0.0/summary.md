# p010_tita_flash_sac_193248_068255_model_5000_kick+0.0

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p010_tita_flash_sac_193248_068255_model_5000_kick+0.0",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "484bf81443fddad9d00ceedf10c942b74f301a835707c7b0c13fec9351747b7a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20081243816575983,
  "max_drift_m": 0.20241354426188318,
  "radial_IAE_m_s": 11.502910273766652,
  "signed_longitudinal_delta_m": -0.20077395837769987,
  "tail_speed_mean_m_s": 3.613441817139975e-05,
  "tail_speed_rms_m_s": 3.617554916207872e-05,
  "tail_sensor_speed_mean_m_s": 3.267321077245358e-05,
  "tail_fk_speed_mean_m_s": 2.7413954378088917e-05,
  "peak_tilt_rad": 0.07525383550129594,
  "peak_wheel_torque_nm": 0.8700644373893738,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.011250117609977,
  "final_integral_m_s": -1.011250117609977,
  "elapsed_wall_s": 9.49589843803551
}
```
