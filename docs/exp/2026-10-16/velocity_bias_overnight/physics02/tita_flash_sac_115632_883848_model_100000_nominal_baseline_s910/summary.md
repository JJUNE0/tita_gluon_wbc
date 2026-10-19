# tita_flash_sac_115632_883848_model_100000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "a409b7fe269c81f27a75f2c94fcd3031f992971cec4504e852c8906a7db28c63",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.924948712416493,
  "max_drift_m": 6.924948712416493,
  "radial_IAE_m_s": 210.1456691608242,
  "signed_longitudinal_delta_m": 6.924187487196256,
  "tail_speed_mean_m_s": 0.1127003424637352,
  "tail_speed_rms_m_s": 0.11270124283760112,
  "tail_sensor_speed_mean_m_s": 0.11245613430129836,
  "tail_fk_speed_mean_m_s": 0.11245591457331802,
  "peak_tilt_rad": 0.08946475453604985,
  "peak_wheel_torque_nm": 0.4004267454147339,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.894452770997304
}
```
