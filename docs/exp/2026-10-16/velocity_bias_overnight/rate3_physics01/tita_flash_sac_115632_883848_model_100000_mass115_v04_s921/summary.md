# tita_flash_sac_115632_883848_model_100000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "6a6b0e96fdc61118da73e535a761bf7f858ad58fc53b83f8ac656004fa0dd93b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030222053873244437,
  "max_drift_m": 0.03627124545799959,
  "radial_IAE_m_s": 1.592276499972004,
  "signed_longitudinal_delta_m": -0.030221962002507794,
  "tail_speed_mean_m_s": -0.0001399547918524453,
  "tail_speed_rms_m_s": 0.006477183038779406,
  "tail_sensor_speed_mean_m_s": 0.0003740546085792333,
  "tail_fk_speed_mean_m_s": 0.0001106865971335427,
  "peak_tilt_rad": 0.1141374736365448,
  "peak_wheel_torque_nm": 2.7337467670440674,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.26757448620630264,
  "final_integral_m_s": -0.26757448620630264,
  "elapsed_wall_s": 14.501954626000952
}
```
