# tita_flash_sac_193248_068255_model_45000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "da680945279ce0090714dbed68db8bb4beb012be95b111953fc91d334c46f1e3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021008245432010325,
  "max_drift_m": 0.039958863274497554,
  "radial_IAE_m_s": 1.311174637132238,
  "signed_longitudinal_delta_m": -0.02100780530770468,
  "tail_speed_mean_m_s": 2.3387173650861782e-05,
  "tail_speed_rms_m_s": 2.3391876830359527e-05,
  "tail_sensor_speed_mean_m_s": 2.035422264513461e-05,
  "tail_fk_speed_mean_m_s": 1.699705194400829e-05,
  "peak_tilt_rad": 0.08310121055278952,
  "peak_wheel_torque_nm": 0.525518536567688,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22318249032903006,
  "final_integral_m_s": -0.22321620095947037,
  "elapsed_wall_s": 18.48429577803472
}
```
