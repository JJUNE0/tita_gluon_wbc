# tita_flash_sac_193248_068255_model_55000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "02f36a2a0a95dc1ca4be7c239719181044f2d86010d5ac14ddd2cabaf1c01bb6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025549719959371484,
  "max_drift_m": 0.059977033933434135,
  "radial_IAE_m_s": 1.9269763007279916,
  "signed_longitudinal_delta_m": -0.02554690187655374,
  "tail_speed_mean_m_s": 0.00021579910730097824,
  "tail_speed_rms_m_s": 0.00021581157037478047,
  "tail_sensor_speed_mean_m_s": 0.00021592638417356733,
  "tail_fk_speed_mean_m_s": 0.00021428018789501296,
  "peak_tilt_rad": 0.1371055139681412,
  "peak_wheel_torque_nm": 1.2700622081756592,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3067681818393378,
  "final_integral_m_s": 0.3067681818393378,
  "elapsed_wall_s": 5.0320371449925005
}
```
