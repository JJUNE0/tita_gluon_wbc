# tita_flash_sac_115632_883848_model_5000_mass115_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass115_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "be92ee38bae4e94fa8dcbd04ed5cc08854cc5f98d6a85b4623ac840dfe55ad99",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 6.692967173044485,
  "max_drift_m": 8.661816071121589,
  "radial_IAE_m_s": 1771.9210627501006,
  "signed_longitudinal_delta_m": -5.7973535851768645,
  "tail_speed_mean_m_s": -0.04745037106662629,
  "tail_speed_rms_m_s": 0.047450371096865236,
  "tail_sensor_speed_mean_m_s": -0.04638392986014608,
  "tail_fk_speed_mean_m_s": -0.04660686718278499,
  "peak_tilt_rad": 0.1725815192012381,
  "peak_wheel_torque_nm": 3.0282697677612305,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 74.61643482599175
}
```
