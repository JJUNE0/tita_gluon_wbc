# tita_flash_sac_115632_883848_model_100000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "d6e602e2a55f60f04449cba9a789a6c77b84659b4ea55fd24b0573baa45d76e7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09284181458239782,
  "max_drift_m": 0.17974927819024403,
  "radial_IAE_m_s": 5.5371091768096345,
  "signed_longitudinal_delta_m": 0.09284018951344225,
  "tail_speed_mean_m_s": 9.440942401334188e-05,
  "tail_speed_rms_m_s": 9.485927607400031e-05,
  "tail_sensor_speed_mean_m_s": 9.403108366824629e-05,
  "tail_fk_speed_mean_m_s": 9.40397112279169e-05,
  "peak_tilt_rad": 0.10381892890011835,
  "peak_wheel_torque_nm": 2.455310344696045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5419074302882029,
  "final_integral_m_s": 0.5419074302882029,
  "elapsed_wall_s": 9.108257400046568
}
```
