# tita_flash_sac_193248_068255_model_45000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "9ac6a3a279f4693c704fa539dfac048b371091beb28f09538ad1356c367aef92",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014938839000945585,
  "max_drift_m": 0.026691593019010675,
  "radial_IAE_m_s": 0.931337986069402,
  "signed_longitudinal_delta_m": -0.014938558575075337,
  "tail_speed_mean_m_s": 1.7488682408469016e-05,
  "tail_speed_rms_m_s": 1.748879415360666e-05,
  "tail_sensor_speed_mean_m_s": 5.563494935513974e-06,
  "tail_fk_speed_mean_m_s": 1.5138229850333596e-06,
  "peak_tilt_rad": 0.07358574039114463,
  "peak_wheel_torque_nm": 0.33772334456443787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1634502500680866,
  "final_integral_m_s": -0.1634531850780523,
  "elapsed_wall_s": 19.99109026795486
}
```
