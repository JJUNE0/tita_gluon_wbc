# tita_flash_sac_193248_068255_model_35000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "5a01404f95ea6640dd668904bced13c307a20c4622d0dea9652a8552f74a9f31",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03342119958061656,
  "max_drift_m": 0.05089779121593521,
  "radial_IAE_m_s": 1.999346899357386,
  "signed_longitudinal_delta_m": 0.03341935232662151,
  "tail_speed_mean_m_s": 7.133832716325444e-06,
  "tail_speed_rms_m_s": 7.134797677873591e-06,
  "tail_sensor_speed_mean_m_s": 5.217683997349987e-06,
  "tail_fk_speed_mean_m_s": 2.761174067474827e-06,
  "peak_tilt_rad": 0.06849537874160028,
  "peak_wheel_torque_nm": 0.8640587329864502,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3447236925737581,
  "final_integral_m_s": 0.3447182463321777,
  "elapsed_wall_s": 17.507959035981912
}
```
