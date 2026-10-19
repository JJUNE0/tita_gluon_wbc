# tita_flash_sac_193248_068255_model_45000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "ee20a5dfbb46fcd5db6ff635aa3faa46a88abe17e4b58b2b5ba1d4dab1b43af2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020193543629720537,
  "max_drift_m": 0.03546445137236164,
  "radial_IAE_m_s": 1.248509368800569,
  "signed_longitudinal_delta_m": -0.020190280413511768,
  "tail_speed_mean_m_s": 1.6795842262771617e-05,
  "tail_speed_rms_m_s": 1.679636789808282e-05,
  "tail_sensor_speed_mean_m_s": 1.76928642005626e-05,
  "tail_fk_speed_mean_m_s": 1.521471645340449e-05,
  "peak_tilt_rad": 0.07933387213110987,
  "peak_wheel_torque_nm": 0.5798582434654236,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21089865811201136,
  "final_integral_m_s": -0.21092845300786395,
  "elapsed_wall_s": 7.579963931988459
}
```
