# tita_flash_sac_193248_068255_model_65000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "9e0d2da0dcd91661f5593696165323d0a91b88d7a9e2bb657de34ab3d93330af",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0009738251327468581,
  "max_drift_m": 0.008063930861823944,
  "radial_IAE_m_s": 0.14013649632373984,
  "signed_longitudinal_delta_m": -0.000948597103540691,
  "tail_speed_mean_m_s": 3.817747812271291e-05,
  "tail_speed_rms_m_s": 3.819400577220716e-05,
  "tail_sensor_speed_mean_m_s": 3.789424494434458e-05,
  "tail_fk_speed_mean_m_s": 3.92808718761188e-05,
  "peak_tilt_rad": 0.03720012553642138,
  "peak_wheel_torque_nm": 0.10550437867641449,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03722904754909193,
  "final_integral_m_s": -0.03722904754909193,
  "elapsed_wall_s": 12.0225513309706
}
```
