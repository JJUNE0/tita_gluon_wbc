# tita_flash_sac_193248_068255_model_60000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "dd467018e71d64d78b5d7fa787924b699226b103afbcb29a24074aaa6558f58b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5030657842883736,
  "max_drift_m": 0.5030657842883736,
  "radial_IAE_m_s": 21.884595293516355,
  "signed_longitudinal_delta_m": -0.5029099573823496,
  "tail_speed_mean_m_s": -0.003630385171941592,
  "tail_speed_rms_m_s": 0.0036658385187588634,
  "tail_sensor_speed_mean_m_s": -0.003622414568105507,
  "tail_fk_speed_mean_m_s": -0.0036203431743424253,
  "peak_tilt_rad": 0.034125998644171984,
  "peak_wheel_torque_nm": 1.4944772720336914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.97888229903765
}
```
