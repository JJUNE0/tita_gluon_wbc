# tita_flash_sac_193248_068255_model_45000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "bb9fd4efa66e6333d1de4ce4f6969c725de3212eda8b7ccdf5974297c5ee7c13",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.059362156202551496,
  "max_drift_m": 0.09397835565290254,
  "radial_IAE_m_s": 3.570341104999625,
  "signed_longitudinal_delta_m": -0.05936198160410188,
  "tail_speed_mean_m_s": -1.432235476322981e-06,
  "tail_speed_rms_m_s": 1.433810621761094e-06,
  "tail_sensor_speed_mean_m_s": -1.7048970953349578e-06,
  "tail_fk_speed_mean_m_s": -2.3102676362021254e-06,
  "peak_tilt_rad": 0.15633057979223097,
  "peak_wheel_torque_nm": 1.8478193283081055,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.616283202399758,
  "final_integral_m_s": -0.6162785407927416,
  "elapsed_wall_s": 14.5359622509568
}
```
