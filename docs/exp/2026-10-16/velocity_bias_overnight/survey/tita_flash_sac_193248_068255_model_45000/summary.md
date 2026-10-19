# tita_flash_sac_193248_068255_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "c69d65ae3e1c4ed830e6ebe7b64fd0911a10659f5ff8bc39ea5752a3e598e865",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.370034617473436,
  "max_drift_m": 8.370034617473436,
  "radial_IAE_m_s": 249.17572885763454,
  "signed_longitudinal_delta_m": -8.31554638020601,
  "tail_speed_mean_m_s": -0.1425753574746399,
  "tail_speed_rms_m_s": 0.14257786545914133,
  "tail_sensor_speed_mean_m_s": -0.14237284369630449,
  "tail_fk_speed_mean_m_s": -0.14238692337998227,
  "peak_tilt_rad": 0.02626670030844025,
  "peak_wheel_torque_nm": 0.08150935173034668,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.126631824008655
}
```
