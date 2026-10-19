# tita_flash_sac_193248_068255_model_30000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "52a95bae47cc5cf56b85602b94f748ae63b757087f5d33fced185b9ab6fbdc64",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007432518093649648,
  "max_drift_m": 0.09100651345954748,
  "radial_IAE_m_s": 0.5343664995771463,
  "signed_longitudinal_delta_m": -0.007417675493281148,
  "tail_speed_mean_m_s": -1.4227140505563945e-05,
  "tail_speed_rms_m_s": 1.608366057155324e-05,
  "tail_sensor_speed_mean_m_s": -1.396725518914749e-05,
  "tail_fk_speed_mean_m_s": -1.4265267582282537e-05,
  "peak_tilt_rad": 0.06922110862597086,
  "peak_wheel_torque_nm": 1.5926223993301392,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10969399168290248,
  "final_integral_m_s": 0.10969399168290248,
  "elapsed_wall_s": 9.31316252000397
}
```
