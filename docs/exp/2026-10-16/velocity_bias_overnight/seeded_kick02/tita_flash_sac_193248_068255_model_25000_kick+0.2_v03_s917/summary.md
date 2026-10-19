# tita_flash_sac_193248_068255_model_25000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "13659b33e0e43caeb11a9d0aa4b898cf3b44ac0fcfc1329c499d82621ac0a420",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03446403822383675,
  "max_drift_m": 0.14759239823505946,
  "radial_IAE_m_s": 2.0629813523820575,
  "signed_longitudinal_delta_m": -0.03438233322781307,
  "tail_speed_mean_m_s": -6.749075630183188e-05,
  "tail_speed_rms_m_s": 6.749317179512012e-05,
  "tail_sensor_speed_mean_m_s": -6.679443315817868e-05,
  "tail_fk_speed_mean_m_s": -6.686669132642156e-05,
  "peak_tilt_rad": 0.12625309146559727,
  "peak_wheel_torque_nm": 2.1203842163085938,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3638392954205002,
  "final_integral_m_s": 0.3638392954205002,
  "elapsed_wall_s": 8.781660181994084
}
```
