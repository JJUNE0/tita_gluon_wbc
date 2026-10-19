# tita_flash_sac_115632_883848_model_5000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "57d9c7ea2dafbc50be31e5db26717ba0237b35049d029adfa04b5103856a20e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.047657734560100425,
  "max_drift_m": 0.12829424557703947,
  "radial_IAE_m_s": 2.9857286057912766,
  "signed_longitudinal_delta_m": -0.04763313231942951,
  "tail_speed_mean_m_s": 2.9151730205542417e-05,
  "tail_speed_rms_m_s": 0.0004091538118836523,
  "tail_sensor_speed_mean_m_s": 4.0101848070193655e-05,
  "tail_fk_speed_mean_m_s": 4.1329009943311335e-05,
  "peak_tilt_rad": 0.18173174092454292,
  "peak_wheel_torque_nm": 5.365023136138916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4932423653964783,
  "final_integral_m_s": -0.49312597310556633,
  "elapsed_wall_s": 18.861084591015242
}
```
