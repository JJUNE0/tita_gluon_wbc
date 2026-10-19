# tita_flash_sac_115632_883848_model_100000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "70ed5ef771cb639e8e62f7a3d5e3d522893735e9d8d8d285b81837a51d7f15ac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.450565977189758,
  "max_drift_m": 6.450565977189758,
  "radial_IAE_m_s": 191.32478703295868,
  "signed_longitudinal_delta_m": 6.436629109964737,
  "tail_speed_mean_m_s": 0.10929455366147257,
  "tail_speed_rms_m_s": 0.10929467855880413,
  "tail_sensor_speed_mean_m_s": 0.10905783974038394,
  "tail_fk_speed_mean_m_s": 0.10905741758382205,
  "peak_tilt_rad": 0.08401728239140716,
  "peak_wheel_torque_nm": 1.334362268447876,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.674988395010587
}
```
