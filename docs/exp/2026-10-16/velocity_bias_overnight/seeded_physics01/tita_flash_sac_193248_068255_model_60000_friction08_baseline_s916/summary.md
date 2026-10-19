# tita_flash_sac_193248_068255_model_60000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "ef07208bcf06201be38f50d603dcdc98cff67f8210e01f7f63e51544cba1b788",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.48851362863544556,
  "max_drift_m": 0.48851362863544556,
  "radial_IAE_m_s": 16.630728989759906,
  "signed_longitudinal_delta_m": -0.4879681373388197,
  "tail_speed_mean_m_s": -0.006058730787725972,
  "tail_speed_rms_m_s": 0.0060835396993264585,
  "tail_sensor_speed_mean_m_s": -0.0060456965995321,
  "tail_fk_speed_mean_m_s": -0.0060433393606014645,
  "peak_tilt_rad": 0.033739184554835155,
  "peak_wheel_torque_nm": 0.09740252792835236,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.303266559028998
}
```
