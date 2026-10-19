# tita_flash_sac_193248_068255_model_45000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
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
  "initial_physics_sha256": "da0b37876c9d66d19dcfa9fac1a625c6228c6218686762922014a5ade9ac50be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.207081460779042,
  "max_drift_m": 8.207081460779042,
  "radial_IAE_m_s": 241.83322086641198,
  "signed_longitudinal_delta_m": -8.167869633797446,
  "tail_speed_mean_m_s": -0.14096949170890619,
  "tail_speed_rms_m_s": 0.14097196616418958,
  "tail_sensor_speed_mean_m_s": -0.14076397983699757,
  "tail_fk_speed_mean_m_s": -0.14077559129001452,
  "peak_tilt_rad": 0.03985504732066136,
  "peak_wheel_torque_nm": 0.19173836708068848,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.757494042045437
}
```
