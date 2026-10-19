# tita_flash_sac_193248_068255_model_90000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "a9efb66d125b1748e74513609a5ef9f2cddf917aab3d5b4198130c276e919a9b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015734816063137883,
  "max_drift_m": 0.015966327195145714,
  "radial_IAE_m_s": 0.3976781155053661,
  "signed_longitudinal_delta_m": -0.015725397064518046,
  "tail_speed_mean_m_s": -0.00036972862908613534,
  "tail_speed_rms_m_s": 0.012038559294362842,
  "tail_sensor_speed_mean_m_s": 0.0008537309084915141,
  "tail_fk_speed_mean_m_s": 0.0001807710619727973,
  "peak_tilt_rad": 0.116770182597973,
  "peak_wheel_torque_nm": 5.09549617767334,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04888633095812347,
  "final_integral_m_s": 0.043262202140285984,
  "elapsed_wall_s": 15.325675569009036
}
```
