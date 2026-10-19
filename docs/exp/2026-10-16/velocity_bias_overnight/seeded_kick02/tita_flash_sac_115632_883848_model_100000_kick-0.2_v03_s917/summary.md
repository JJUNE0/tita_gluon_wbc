# tita_flash_sac_115632_883848_model_100000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "00ee4ba35830207947442a9468c4688dd41e255bcdbe91f82943e31c22e1bb19",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08997028554927254,
  "max_drift_m": 0.11564376134473857,
  "radial_IAE_m_s": 5.1261575954758865,
  "signed_longitudinal_delta_m": 0.08996931267159113,
  "tail_speed_mean_m_s": 9.652361070636652e-05,
  "tail_speed_rms_m_s": 9.719261651715455e-05,
  "tail_sensor_speed_mean_m_s": 9.614089385126823e-05,
  "tail_fk_speed_mean_m_s": 9.614661137330427e-05,
  "peak_tilt_rad": 0.0857446939119959,
  "peak_wheel_torque_nm": 1.8887882232666016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5410201846813527,
  "final_integral_m_s": 0.5410201846813527,
  "elapsed_wall_s": 8.870016140979715
}
```
