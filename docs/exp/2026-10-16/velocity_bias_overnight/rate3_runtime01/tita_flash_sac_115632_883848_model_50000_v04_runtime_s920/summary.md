# tita_flash_sac_115632_883848_model_50000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "c18d8e66a5c43b8c6ff4bb7b3e116cf2b3835b35b7ab0ffaf6660aec428c92d6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0032176834138268333,
  "max_drift_m": 0.005825623214696897,
  "radial_IAE_m_s": 0.19403549448475402,
  "signed_longitudinal_delta_m": -0.0031056969336327083,
  "tail_speed_mean_m_s": 3.437934267625344e-06,
  "tail_speed_rms_m_s": 6.161351582784764e-06,
  "tail_sensor_speed_mean_m_s": 3.604843495287257e-06,
  "tail_fk_speed_mean_m_s": 6.029024998285364e-06,
  "peak_tilt_rad": 0.04181295895851611,
  "peak_wheel_torque_nm": 0.3275783956050873,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021373675857601502,
  "final_integral_m_s": 0.021373675857601502,
  "elapsed_wall_s": 11.779286230972502
}
```
