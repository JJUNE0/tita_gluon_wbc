# tita_flash_sac_115632_883848_model_100000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "721487adc3db010c2e185fe40d149ece4c0f76eaecfdf387c6614e60bd571b15",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.3664284474733135,
  "max_drift_m": 3.3664284474733135,
  "radial_IAE_m_s": 101.71922448156685,
  "signed_longitudinal_delta_m": -3.3654806236007597,
  "tail_speed_mean_m_s": -0.05531793556203185,
  "tail_speed_rms_m_s": 0.05531840893780386,
  "tail_sensor_speed_mean_m_s": -0.05520446357849415,
  "tail_fk_speed_mean_m_s": -0.055204096696324756,
  "peak_tilt_rad": 0.08295969576313666,
  "peak_wheel_torque_nm": 0.5211188197135925,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.329082084004767
}
```
