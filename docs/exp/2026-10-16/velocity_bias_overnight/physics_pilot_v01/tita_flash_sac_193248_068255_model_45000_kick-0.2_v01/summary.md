# tita_flash_sac_193248_068255_model_45000_kick-0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "452c4137ff4b72e04ee38c62768ee03a7044f1ab4bf9bb5f407cdcfa97c922ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020541440515921678,
  "max_drift_m": 0.14605382537987013,
  "radial_IAE_m_s": 1.366178352727161,
  "signed_longitudinal_delta_m": -0.02048980340640317,
  "tail_speed_mean_m_s": 1.65023317784592e-05,
  "tail_speed_rms_m_s": 1.650283876794543e-05,
  "tail_sensor_speed_mean_m_s": 1.7340996825230232e-05,
  "tail_fk_speed_mean_m_s": 1.4874679212436964e-05,
  "peak_tilt_rad": 0.1639253802648697,
  "peak_wheel_torque_nm": 2.4089202880859375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20881899513286642,
  "final_integral_m_s": -0.20884819130648874,
  "elapsed_wall_s": 4.72418740298599
}
```
