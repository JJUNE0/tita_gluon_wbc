# tita_flash_sac_115632_883848_model_10000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "0711504c1f928c40e00afb6588e53fbb2dc249ec26b88a8e2d6b9237eed8306b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0078198067517403,
  "max_drift_m": 1.0078198067517403,
  "radial_IAE_m_s": 32.35224206479664,
  "signed_longitudinal_delta_m": 1.0073529787009194,
  "tail_speed_mean_m_s": 0.014643276420958007,
  "tail_speed_rms_m_s": 0.01654329036115895,
  "tail_sensor_speed_mean_m_s": 0.015645705116587805,
  "tail_fk_speed_mean_m_s": 0.014449443261374198,
  "peak_tilt_rad": 0.1085056502054611,
  "peak_wheel_torque_nm": 2.8189961910247803,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.970953162002843
}
```
