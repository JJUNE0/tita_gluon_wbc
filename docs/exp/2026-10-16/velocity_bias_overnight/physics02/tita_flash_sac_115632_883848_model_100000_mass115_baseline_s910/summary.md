# tita_flash_sac_115632_883848_model_100000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "cdc1ca16b7ccfc546e34a988c70bf9ec3aaaa7058731a821a731a322d61acb15",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.5140956120034352,
  "max_drift_m": 3.5140956120034352,
  "radial_IAE_m_s": 105.93027360768691,
  "signed_longitudinal_delta_m": -3.51234360842737,
  "tail_speed_mean_m_s": -0.05796651863969831,
  "tail_speed_rms_m_s": 0.05796696533007008,
  "tail_sensor_speed_mean_m_s": -0.05784175546653254,
  "tail_fk_speed_mean_m_s": -0.05784097913116538,
  "peak_tilt_rad": 0.08184310870634315,
  "peak_wheel_torque_nm": 0.5638871192932129,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.27493683702778
}
```
