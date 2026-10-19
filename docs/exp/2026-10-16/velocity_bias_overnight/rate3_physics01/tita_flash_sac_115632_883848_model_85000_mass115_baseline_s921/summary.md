# tita_flash_sac_115632_883848_model_85000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "initial_physics_sha256": "0f7b4498aa7d2094b9217b821088fde011c0e7488480048b94f026bdd5a3f1ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7766615718526964,
  "max_drift_m": 1.7766615718526964,
  "radial_IAE_m_s": 53.43014664157121,
  "signed_longitudinal_delta_m": -1.7762318295299708,
  "tail_speed_mean_m_s": -0.029550301647691762,
  "tail_speed_rms_m_s": 0.029550302234927005,
  "tail_sensor_speed_mean_m_s": -0.029486902373735403,
  "tail_fk_speed_mean_m_s": -0.02948688877775675,
  "peak_tilt_rad": 0.05976811655375536,
  "peak_wheel_torque_nm": 0.13469943404197693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.084937367995735
}
```
