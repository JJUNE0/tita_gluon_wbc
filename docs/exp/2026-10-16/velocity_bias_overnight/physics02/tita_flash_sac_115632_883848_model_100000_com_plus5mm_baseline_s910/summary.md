# tita_flash_sac_115632_883848_model_100000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "7eda3ed9698619490c7e56b5cfb17a5a1bbf8b5ca36f95bb86fcfdfdf5364107",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.996691813607536,
  "max_drift_m": 7.996691813607536,
  "radial_IAE_m_s": 242.99352226376746,
  "signed_longitudinal_delta_m": 7.996294171962163,
  "tail_speed_mean_m_s": 0.13002530185874428,
  "tail_speed_rms_m_s": 0.13002712133363079,
  "tail_sensor_speed_mean_m_s": 0.12977783661875572,
  "tail_fk_speed_mean_m_s": 0.12974472796395728,
  "peak_tilt_rad": 0.0898373715405858,
  "peak_wheel_torque_nm": 0.3910685181617737,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.36719479097519
}
```
