# tita_flash_sac_115632_883848_model_70000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "23dedde4d54d6620df8a90d3c844e4bc1718cb479df9ab54733b0ad8d45c180b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015118159310029628,
  "max_drift_m": 0.029867110681994158,
  "radial_IAE_m_s": 0.9111131135615975,
  "signed_longitudinal_delta_m": -0.015073496252431888,
  "tail_speed_mean_m_s": -1.6678600375830671e-06,
  "tail_speed_rms_m_s": 1.6856105306360886e-06,
  "tail_sensor_speed_mean_m_s": -1.7211848961217046e-06,
  "tail_fk_speed_mean_m_s": -1.5843257528268817e-06,
  "peak_tilt_rad": 0.05066351399831648,
  "peak_wheel_torque_nm": 0.46876341104507446,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15750457744557014,
  "final_integral_m_s": -0.15750177526031667,
  "elapsed_wall_s": 11.323726597998757
}
```
