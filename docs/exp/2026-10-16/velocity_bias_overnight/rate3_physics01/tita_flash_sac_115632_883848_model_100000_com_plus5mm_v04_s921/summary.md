# tita_flash_sac_115632_883848_model_100000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "1e86e2de162518ca37e240477bc35c926864e1c4ae30cce713d8b251fd15b454",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0913514184302892,
  "max_drift_m": 0.12084532396509991,
  "radial_IAE_m_s": 5.368284296273921,
  "signed_longitudinal_delta_m": 0.09135070225594398,
  "tail_speed_mean_m_s": 6.393058195040218e-05,
  "tail_speed_rms_m_s": 6.599101962724812e-05,
  "tail_sensor_speed_mean_m_s": 6.368218286528466e-05,
  "tail_fk_speed_mean_m_s": 6.348106775898398e-05,
  "peak_tilt_rad": 0.08600456601544959,
  "peak_wheel_torque_nm": 0.5803574919700623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6018758478665567,
  "final_integral_m_s": 0.6018758478665567,
  "elapsed_wall_s": 13.085733960964717
}
```
