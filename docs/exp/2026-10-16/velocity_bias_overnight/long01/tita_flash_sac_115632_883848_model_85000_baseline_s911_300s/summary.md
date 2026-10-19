# tita_flash_sac_115632_883848_model_85000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "f4cf662d676d1d1388509ca848ff299dbeb51b25bd94fc13372e0ccf234f7659",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 39.00009499466325,
  "max_drift_m": 39.00009499466325,
  "radial_IAE_m_s": 5778.334564577205,
  "signed_longitudinal_delta_m": 38.76487377419906,
  "tail_speed_mean_m_s": 0.1322494145611781,
  "tail_speed_rms_m_s": 0.13224941461540007,
  "tail_sensor_speed_mean_m_s": 0.13196299971300302,
  "tail_fk_speed_mean_m_s": 0.13196310073006404,
  "peak_tilt_rad": 0.06759991485948125,
  "peak_wheel_torque_nm": 0.157696932554245,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 43.55568024102831
}
```
