# tita_flash_sac_193248_068255_model_55000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "b8140b72c0344490998c7e40faddf73fc28e8566aa7a3f49e882383543df1d99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.913933596145753,
  "max_drift_m": 3.913933596145753,
  "radial_IAE_m_s": 116.07889551643814,
  "signed_longitudinal_delta_m": 3.912285475563931,
  "tail_speed_mean_m_s": 0.06641576639261605,
  "tail_speed_rms_m_s": 0.06641589948045622,
  "tail_sensor_speed_mean_m_s": 0.06627322564693396,
  "tail_fk_speed_mean_m_s": 0.06627265317849944,
  "peak_tilt_rad": 0.18295838622882687,
  "peak_wheel_torque_nm": 0.36524078249931335,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.401511645992287
}
```
