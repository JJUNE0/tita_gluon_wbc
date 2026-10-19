# tita_flash_sac_193248_068255_model_90000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "df5fcf127cae1dac715f947840249db93cf5da78ce7c4e8360786adb1d75ce39",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.072511604907268,
  "max_drift_m": 13.072511604907268,
  "radial_IAE_m_s": 384.8809184270891,
  "signed_longitudinal_delta_m": 13.063768645195365,
  "tail_speed_mean_m_s": 0.22355317494573979,
  "tail_speed_rms_m_s": 0.22355327559940222,
  "tail_sensor_speed_mean_m_s": 0.2230696276061611,
  "tail_fk_speed_mean_m_s": 0.22306727379922417,
  "peak_tilt_rad": 0.11198476758631615,
  "peak_wheel_torque_nm": 1.950643539428711,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.110781128983945
}
```
