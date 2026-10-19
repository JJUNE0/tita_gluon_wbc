# tita_flash_sac_193248_068255_model_75000_com_minus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_minus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "bfeb561ff86ebd7992f0e6e6bc5acf85a7105e0f9ef148092da36f7ffc1e12d9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 19.807871551919956,
  "max_drift_m": 19.807871551919956,
  "radial_IAE_m_s": 3702.837961596184,
  "signed_longitudinal_delta_m": -7.54767901968975,
  "tail_speed_mean_m_s": -0.34024377462137445,
  "tail_speed_rms_m_s": 0.3402437796520417,
  "tail_sensor_speed_mean_m_s": -0.33963961286678396,
  "tail_fk_speed_mean_m_s": -0.339671351097385,
  "peak_tilt_rad": 0.041381444764133635,
  "peak_wheel_torque_nm": 0.2574247717857361,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 27.3357410649769
}
```
