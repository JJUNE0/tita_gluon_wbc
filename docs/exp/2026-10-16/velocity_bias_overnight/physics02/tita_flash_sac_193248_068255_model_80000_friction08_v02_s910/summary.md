# tita_flash_sac_193248_068255_model_80000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "c7f00ec40e77ba15f15396f744042a8053fd4f8b96053a4aac521f56241968b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006329066515753274,
  "max_drift_m": 0.008017051233499297,
  "radial_IAE_m_s": 0.3529603613481268,
  "signed_longitudinal_delta_m": 0.006288811835096962,
  "tail_speed_mean_m_s": 2.4640047060039494e-05,
  "tail_speed_rms_m_s": 0.00279577517854729,
  "tail_sensor_speed_mean_m_s": 0.00024226928158899922,
  "tail_fk_speed_mean_m_s": 0.00015663328381430175,
  "peak_tilt_rad": 0.05026526012607713,
  "peak_wheel_torque_nm": 2.4967916011810303,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1151818600134425,
  "final_integral_m_s": 0.10616483445325323,
  "elapsed_wall_s": 13.265830090967938
}
```
