# tita_flash_sac_115632_883848_model_100000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "a890090183bc2f09c0f7e3e791deabd6d0f4cb5978b547e15e0d937a84821616",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.893375037261967,
  "max_drift_m": 6.893375037261967,
  "radial_IAE_m_s": 209.66385852481645,
  "signed_longitudinal_delta_m": 6.889331089267149,
  "tail_speed_mean_m_s": 0.11224836694427488,
  "tail_speed_rms_m_s": 0.11224894301749232,
  "tail_sensor_speed_mean_m_s": 0.11200517687099298,
  "tail_fk_speed_mean_m_s": 0.11200483694818948,
  "peak_tilt_rad": 0.08845591493224769,
  "peak_wheel_torque_nm": 0.15377014875411987,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.483076686039567
}
```
