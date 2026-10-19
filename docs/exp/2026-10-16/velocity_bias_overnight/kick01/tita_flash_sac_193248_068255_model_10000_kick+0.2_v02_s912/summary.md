# tita_flash_sac_193248_068255_model_10000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "a2b6ee02ca7927eea13675610b35b7d3363db46a783a01a2bc306494aefb47da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011985518481398089,
  "max_drift_m": 0.05159698028618982,
  "radial_IAE_m_s": 0.6898177268417947,
  "signed_longitudinal_delta_m": 0.011940431703104876,
  "tail_speed_mean_m_s": 5.444977645618948e-05,
  "tail_speed_rms_m_s": 5.447612466833937e-05,
  "tail_sensor_speed_mean_m_s": 6.691598959670557e-05,
  "tail_fk_speed_mean_m_s": 7.337740233791639e-05,
  "peak_tilt_rad": 0.08228689627734842,
  "peak_wheel_torque_nm": 2.4260671138763428,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.13350030762995269,
  "final_integral_m_s": 0.13335276575146818,
  "elapsed_wall_s": 12.912349071993958
}
```
