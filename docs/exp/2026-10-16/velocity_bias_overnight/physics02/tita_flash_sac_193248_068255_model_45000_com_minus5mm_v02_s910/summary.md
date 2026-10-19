# tita_flash_sac_193248_068255_model_45000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "5bdcd5e3797b940c8b5d89a4921634443eec5f551a10d2cf9b60caca7d4c0028",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025436501873452425,
  "max_drift_m": 0.04977816997279142,
  "radial_IAE_m_s": 1.5658683453997289,
  "signed_longitudinal_delta_m": -0.025435960284025685,
  "tail_speed_mean_m_s": 1.581319603574163e-05,
  "tail_speed_rms_m_s": 1.5815497766309826e-05,
  "tail_sensor_speed_mean_m_s": 1.6700965091275585e-05,
  "tail_fk_speed_mean_m_s": 1.4035599558396684e-05,
  "peak_tilt_rad": 0.09031196678744458,
  "peak_wheel_torque_nm": 0.631244421005249,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.26754619942237406,
  "final_integral_m_s": -0.26757398485726613,
  "elapsed_wall_s": 15.374609552964102
}
```
