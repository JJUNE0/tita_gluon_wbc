# tita_flash_sac_193248_068255_model_80000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "c74e4c4932de6c12714f01f05fbb23b1e62ed499e6e1e1a13d18b65785618c5a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06962622917600021,
  "max_drift_m": 0.1291373392404342,
  "radial_IAE_m_s": 6.2157189491001,
  "signed_longitudinal_delta_m": -0.06960994169361984,
  "tail_speed_mean_m_s": 0.0027151587337080844,
  "tail_speed_rms_m_s": 0.003828236043109561,
  "tail_sensor_speed_mean_m_s": 0.0024710385870966773,
  "tail_fk_speed_mean_m_s": 0.002834863837095604,
  "peak_tilt_rad": 0.04913646471756539,
  "peak_wheel_torque_nm": 2.1132490634918213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.029555984016042
}
```
