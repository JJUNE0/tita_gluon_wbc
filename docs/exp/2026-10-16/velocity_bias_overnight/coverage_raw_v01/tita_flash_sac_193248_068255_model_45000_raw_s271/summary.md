# tita_flash_sac_193248_068255_model_45000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "42a41b2d61b6cff6833d67bc947fde8bd7941229c4adee412a50ca5bf41ee96c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02302777390602918,
  "max_drift_m": 0.05533448678057693,
  "radial_IAE_m_s": 1.311875352355378,
  "signed_longitudinal_delta_m": -0.023026590919572102,
  "tail_speed_mean_m_s": -3.8084588237981745e-05,
  "tail_speed_rms_m_s": 0.007161496776347744,
  "tail_sensor_speed_mean_m_s": 8.225276487767834e-05,
  "tail_fk_speed_mean_m_s": 4.4924511780060786e-05,
  "peak_tilt_rad": 0.12267686358445684,
  "peak_wheel_torque_nm": 1.638840675354004,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.33580102791010574,
  "final_integral_m_s": -0.28491850047382106,
  "elapsed_wall_s": 4.410466899047606
}
```
