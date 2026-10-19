# tita_flash_sac_115632_883848_model_50000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "f1deb2428568cc7c6d03beeb051d1f576c5638fd56482d9a18c9a0716128ed85",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005567521541910799,
  "max_drift_m": 0.08211352629332531,
  "radial_IAE_m_s": 0.4438155837824492,
  "signed_longitudinal_delta_m": -0.004587491820672198,
  "tail_speed_mean_m_s": 3.589542218013217e-06,
  "tail_speed_rms_m_s": 6.286354973212653e-06,
  "tail_sensor_speed_mean_m_s": 3.7532035393600578e-06,
  "tail_fk_speed_mean_m_s": 6.179131270466007e-06,
  "peak_tilt_rad": 0.08094138557184438,
  "peak_wheel_torque_nm": 1.367788314819336,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02137100791004181,
  "final_integral_m_s": 0.02137100791004181,
  "elapsed_wall_s": 13.67811946402071
}
```
