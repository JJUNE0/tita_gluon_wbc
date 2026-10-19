# tita_flash_sac_115632_883848_model_100000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "81cd2ed55ef5b611eea3aef950b78b582261e99a93c2cb8f613c05ebf04b5a8d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.053526246580637114,
  "max_drift_m": 0.07302287454390757,
  "radial_IAE_m_s": 3.139040666934873,
  "signed_longitudinal_delta_m": 0.053525517077443116,
  "tail_speed_mean_m_s": 3.808989494848562e-05,
  "tail_speed_rms_m_s": 3.829763238827085e-05,
  "tail_sensor_speed_mean_m_s": 3.7836122265811145e-05,
  "tail_fk_speed_mean_m_s": 3.7840085716869926e-05,
  "peak_tilt_rad": 0.0856434079110564,
  "peak_wheel_torque_nm": 0.5026266574859619,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5416658006095437,
  "final_integral_m_s": 0.5415896827378871,
  "elapsed_wall_s": 6.29514649201883
}
```
