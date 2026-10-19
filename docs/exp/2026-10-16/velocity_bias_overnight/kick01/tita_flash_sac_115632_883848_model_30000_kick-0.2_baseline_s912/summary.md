# tita_flash_sac_115632_883848_model_30000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "14a85fce3ef5e3eeb5929054fba5c07788f40aca610f33005a5ec16aab13bb4d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.927608473523112,
  "max_drift_m": 13.927608473523112,
  "radial_IAE_m_s": 418.0663723831747,
  "signed_longitudinal_delta_m": 13.904906432006605,
  "tail_speed_mean_m_s": 0.23133275984943552,
  "tail_speed_rms_m_s": 0.23133284839240573,
  "tail_sensor_speed_mean_m_s": 0.23083166427679738,
  "tail_fk_speed_mean_m_s": 0.23083007221310162,
  "peak_tilt_rad": 0.12664607403404293,
  "peak_wheel_torque_nm": 1.5469958782196045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.554126831004396
}
```
