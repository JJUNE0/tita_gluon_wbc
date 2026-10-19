# tita_flash_sac_193248_068255_model_45000_kick-0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "452c4137ff4b72e04ee38c62768ee03a7044f1ab4bf9bb5f407cdcfa97c922ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.52057224515461,
  "max_drift_m": 8.52057224515461,
  "radial_IAE_m_s": 258.93184995072215,
  "signed_longitudinal_delta_m": -8.468356224498962,
  "tail_speed_mean_m_s": -0.14200730346786328,
  "tail_speed_rms_m_s": 0.14201008773076304,
  "tail_sensor_speed_mean_m_s": -0.14180338316246485,
  "tail_fk_speed_mean_m_s": -0.14181620200035025,
  "peak_tilt_rad": 0.02626675985873117,
  "peak_wheel_torque_nm": 1.577871322631836,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.703189540014137
}
```
