# tita_flash_sac_193248_068255_model_45000_kick+0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick+0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
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
  "initial_physics_sha256": "ee50e80c8573f406d0b1b7f6f379a3679504a16d309f01a960e1e8c7c1506d96",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.113889486919607,
  "max_drift_m": 8.113889486919607,
  "radial_IAE_m_s": 234.62951871750352,
  "signed_longitudinal_delta_m": -8.065512874653146,
  "tail_speed_mean_m_s": -0.1421763435417436,
  "tail_speed_rms_m_s": 0.14217910087733626,
  "tail_sensor_speed_mean_m_s": -0.14197297975374887,
  "tail_fk_speed_mean_m_s": -0.14198593159740783,
  "peak_tilt_rad": 0.056981285279415594,
  "peak_wheel_torque_nm": 1.355190396308899,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.784495874017011
}
```
