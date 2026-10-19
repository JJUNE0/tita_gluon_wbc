# tita_flash_sac_193248_068255_model_30000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "d71362303e21cbf731a79bdc973f29dd9186a57b4926901be8702af8278fb89e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011584620160926793,
  "max_drift_m": 0.023758645718668644,
  "radial_IAE_m_s": 0.7096053331127803,
  "signed_longitudinal_delta_m": 0.011584228564508863,
  "tail_speed_mean_m_s": -5.9400594490660845e-06,
  "tail_speed_rms_m_s": 5.940740642369468e-06,
  "tail_sensor_speed_mean_m_s": -5.4641334424807936e-06,
  "tail_fk_speed_mean_m_s": -5.465707137680857e-06,
  "peak_tilt_rad": 0.03575044109775649,
  "peak_wheel_torque_nm": 0.5278482437133789,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12303219717247346,
  "final_integral_m_s": 0.12304279729507404,
  "elapsed_wall_s": 24.059219058952294
}
```
