# tita_flash_sac_193248_068255_model_45000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "9c8f42bd32a9f2428a0e00d6973b5e36eb0b1276649da7cb7bd8dc7af98ed253",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01691314142595415,
  "max_drift_m": 0.037527723239128674,
  "radial_IAE_m_s": 5.67520402724575,
  "signed_longitudinal_delta_m": -0.01690995523520134,
  "tail_speed_mean_m_s": 1.2457542445708036e-05,
  "tail_speed_rms_m_s": 1.2458014967523936e-05,
  "tail_sensor_speed_mean_m_s": 1.2663809392714188e-05,
  "tail_fk_speed_mean_m_s": 1.0331623893030528e-05,
  "peak_tilt_rad": 0.08136115174903247,
  "peak_wheel_torque_nm": 0.49254971742630005,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18192644562645546,
  "final_integral_m_s": -0.18194671827012257,
  "elapsed_wall_s": 77.60309592599515
}
```
