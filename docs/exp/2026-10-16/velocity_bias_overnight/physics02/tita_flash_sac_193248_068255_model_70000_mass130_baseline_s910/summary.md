# tita_flash_sac_193248_068255_model_70000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "382f10a02dbabd88d98bf60a5215d4c235247db8260e156e409d591cde001bf5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.32173738378918,
  "max_drift_m": 13.32173738378918,
  "radial_IAE_m_s": 394.8430830517583,
  "signed_longitudinal_delta_m": -13.2920407418456,
  "tail_speed_mean_m_s": -0.228756037940772,
  "tail_speed_rms_m_s": 0.22876048761439635,
  "tail_sensor_speed_mean_m_s": -0.2284123056123209,
  "tail_fk_speed_mean_m_s": -0.2284164284544886,
  "peak_tilt_rad": 0.07437578542614354,
  "peak_wheel_torque_nm": 0.8147603273391724,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.58773927000584
}
```
