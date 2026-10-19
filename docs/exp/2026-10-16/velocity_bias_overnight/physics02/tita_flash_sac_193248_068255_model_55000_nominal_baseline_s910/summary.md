# tita_flash_sac_193248_068255_model_55000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "a602b02259d723f7309dc5fc9d2f3eb0ba8c3b6cb65c377389e9db7e14ef85ec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 18.506681666880716,
  "max_drift_m": 18.506681666880716,
  "radial_IAE_m_s": 536.0390813895814,
  "signed_longitudinal_delta_m": 18.267416604561543,
  "tail_speed_mean_m_s": 0.3240756885936536,
  "tail_speed_rms_m_s": 0.32407569002332826,
  "tail_sensor_speed_mean_m_s": 0.323374963806619,
  "tail_fk_speed_mean_m_s": 0.3233682385077976,
  "peak_tilt_rad": 0.17354748986284507,
  "peak_wheel_torque_nm": 0.25728070735931396,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.088954474020284
}
```
