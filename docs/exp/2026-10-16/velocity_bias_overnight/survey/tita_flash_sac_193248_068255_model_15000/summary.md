# tita_flash_sac_193248_068255_model_15000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "d87f0e5d38f618295f22772666275a087e5fb28fc29714180de99fbc2afdffec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.4234083068054026,
  "max_drift_m": 3.4234083068054026,
  "radial_IAE_m_s": 102.9701804922622,
  "signed_longitudinal_delta_m": -3.423369794829227,
  "tail_speed_mean_m_s": -0.05675897906694905,
  "tail_speed_rms_m_s": 0.0567590324835926,
  "tail_sensor_speed_mean_m_s": -0.05666999768599788,
  "tail_fk_speed_mean_m_s": -0.05667013534927015,
  "peak_tilt_rad": 0.04415659938358507,
  "peak_wheel_torque_nm": 0.03483772277832031,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.391392096003983
}
```
