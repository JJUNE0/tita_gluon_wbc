# tita_flash_sac_115632_883848_model_50000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "2b4a12fa7b5d78c0715d6ad66f626dcd042ad4ae82c05ff1d278e8ee28c2d44d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0031090950617320267,
  "max_drift_m": 0.0041907691338563605,
  "radial_IAE_m_s": 0.15283589208652992,
  "signed_longitudinal_delta_m": -0.002406720284513022,
  "tail_speed_mean_m_s": -1.962455662382381e-06,
  "tail_speed_rms_m_s": 1.984499037327709e-06,
  "tail_sensor_speed_mean_m_s": -1.7843669196167297e-06,
  "tail_fk_speed_mean_m_s": 7.001863145356325e-07,
  "peak_tilt_rad": 0.04164948094190879,
  "peak_wheel_torque_nm": 0.2968749403953552,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.01813121491138059,
  "final_integral_m_s": -0.01813205931675541,
  "elapsed_wall_s": 12.252333514974453
}
```
