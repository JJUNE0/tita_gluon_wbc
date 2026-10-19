# tita_flash_sac_115632_883848_model_100000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "6a6b0e96fdc61118da73e535a761bf7f858ad58fc53b83f8ac656004fa0dd93b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.3664259568007493,
  "max_drift_m": 3.3664259568007493,
  "radial_IAE_m_s": 101.71915541158786,
  "signed_longitudinal_delta_m": -3.3654781447980993,
  "tail_speed_mean_m_s": -0.055317888962672944,
  "tail_speed_rms_m_s": 0.055318362342059446,
  "tail_sensor_speed_mean_m_s": -0.0552044157407961,
  "tail_fk_speed_mean_m_s": -0.055204050339397855,
  "peak_tilt_rad": 0.08295971472865427,
  "peak_wheel_torque_nm": 0.5211189389228821,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.200270818022545
}
```
