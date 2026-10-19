# tita_flash_sac_115632_883848_model_5000_mass130_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass130_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
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
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "5ff53c3fc6ad9ac333531bc02f01b003a6304c51055ebf84aa79fb7e8802f301",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.15504094562644644,
  "max_drift_m": 0.1585501611899969,
  "radial_IAE_m_s": 25.986112704718053,
  "signed_longitudinal_delta_m": -0.15143766967749425,
  "tail_speed_mean_m_s": -0.00043156370747054763,
  "tail_speed_rms_m_s": 0.019491156880813838,
  "tail_sensor_speed_mean_m_s": -0.0005337103688347533,
  "tail_fk_speed_mean_m_s": 1.3008782989259372e-05,
  "peak_tilt_rad": 0.18482059954049213,
  "peak_wheel_torque_nm": 3.704315662384033,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.13704620636487277,
  "final_integral_m_s": -0.15011063339250164,
  "elapsed_wall_s": 92.68324306997238
}
```
