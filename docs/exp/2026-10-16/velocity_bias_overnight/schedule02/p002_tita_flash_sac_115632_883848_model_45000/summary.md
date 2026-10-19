# p002_tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
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
      "slew": 2.0,
      "gain_velocity": 0.05,
      "gain_tau": 0.6,
      "gain_floor": 0.1
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "3a4ba1ca68189c8896b3491841cd28abf61e8aa5305f036f14ac64ec8a9f372d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02083336250864478,
  "max_drift_m": 0.07138197366178936,
  "radial_IAE_m_s": 1.0093315086735948,
  "signed_longitudinal_delta_m": -0.020828165413702537,
  "tail_speed_mean_m_s": -0.00018274821472548717,
  "tail_speed_rms_m_s": 0.0001828719055326493,
  "tail_sensor_speed_mean_m_s": -0.00018196747556787333,
  "tail_fk_speed_mean_m_s": -0.00017990476312586482,
  "peak_tilt_rad": 0.12854289379896233,
  "peak_wheel_torque_nm": 1.9890872240066528,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35047256744766814,
  "final_integral_m_s": -0.3504402901826789,
  "elapsed_wall_s": 13.08261741901515
}
```
