# tita_flash_sac_115632_883848_model_100000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "eb3e8838edbb7e03a460b7bdf86c93fae8f660cfe22fd6933f9cbc65440a4f55",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0890862550750905,
  "max_drift_m": 0.1056588802933384,
  "radial_IAE_m_s": 5.10973482604881,
  "signed_longitudinal_delta_m": 0.08908612036745334,
  "tail_speed_mean_m_s": 0.00010816480037713961,
  "tail_speed_rms_m_s": 0.00010818311957004006,
  "tail_sensor_speed_mean_m_s": 0.00010779750351819324,
  "tail_fk_speed_mean_m_s": 0.00010782880448792307,
  "peak_tilt_rad": 0.08310001628080688,
  "peak_wheel_torque_nm": 0.4046100378036499,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4689066931856116,
  "final_integral_m_s": 0.4689066931856116,
  "elapsed_wall_s": 14.67704457900254
}
```
