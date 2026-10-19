# tita_flash_sac_193248_068255_model_85000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
  },
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "b221819ed103389dd3319648e601ef84b20f782410429b3304173659dac213ba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0026978506341535017,
  "max_drift_m": 0.04232502797787846,
  "radial_IAE_m_s": 0.326434094326908,
  "signed_longitudinal_delta_m": 0.0026975939150461164,
  "tail_speed_mean_m_s": 0.00013442568192539173,
  "tail_speed_rms_m_s": 0.00039166425246399953,
  "tail_sensor_speed_mean_m_s": 0.00013779654058085504,
  "tail_fk_speed_mean_m_s": 0.0001339217360684026,
  "peak_tilt_rad": 0.0599927718467399,
  "peak_wheel_torque_nm": 0.5936912298202515,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19466719910939365,
  "final_integral_m_s": 0.19466719910939365,
  "elapsed_wall_s": 13.917593150981702
}
```
