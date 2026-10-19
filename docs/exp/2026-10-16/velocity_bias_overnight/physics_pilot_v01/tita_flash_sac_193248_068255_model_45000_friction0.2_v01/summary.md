# tita_flash_sac_193248_068255_model_45000_friction0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "0821009f8b3eb6ab1943b3c81cd0bf04075b629c64db7a76bcfe1d1b7aeffda1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013830124111746755,
  "max_drift_m": 0.044564143683613236,
  "radial_IAE_m_s": 0.8801995360679289,
  "signed_longitudinal_delta_m": -0.013821114241877661,
  "tail_speed_mean_m_s": 1.7770390062530914e-05,
  "tail_speed_rms_m_s": 1.7770462079914975e-05,
  "tail_sensor_speed_mean_m_s": 5.18299967796607e-06,
  "tail_fk_speed_mean_m_s": 1.0304842252957316e-06,
  "peak_tilt_rad": 0.090385158421745,
  "peak_wheel_torque_nm": 0.8523290157318115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1623263268769865,
  "final_integral_m_s": -0.16232826828562064,
  "elapsed_wall_s": 5.379942235013004
}
```
