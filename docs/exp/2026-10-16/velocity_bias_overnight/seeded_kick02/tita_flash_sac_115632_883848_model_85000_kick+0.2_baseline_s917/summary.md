# tita_flash_sac_115632_883848_model_85000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "85772d58d24ff10728334de5a3ac66d06f4111ace138ba5f330e2b5919cf8585",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.593881328406321,
  "max_drift_m": 7.593881328406321,
  "radial_IAE_m_s": 228.86758843500144,
  "signed_longitudinal_delta_m": 7.578282490127117,
  "tail_speed_mean_m_s": 0.12741259792659268,
  "tail_speed_rms_m_s": 0.12741426134054537,
  "tail_sensor_speed_mean_m_s": 0.1271370813904493,
  "tail_fk_speed_mean_m_s": 0.1271372782665039,
  "peak_tilt_rad": 0.08208413470807852,
  "peak_wheel_torque_nm": 1.9680886268615723,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.043523393047508
}
```
