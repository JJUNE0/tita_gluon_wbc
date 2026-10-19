# tita_flash_sac_193248_068255_model_75000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "1fcd56bc99c4746ef9666921faf80980d5f02af3ec4982694f65ffb563da8f6e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 4.305309539279952,
  "max_drift_m": 17.41627975442308,
  "radial_IAE_m_s": 2522.179765129533,
  "signed_longitudinal_delta_m": -2.3288192579009257,
  "tail_speed_mean_m_s": -0.012413336348206416,
  "tail_speed_rms_m_s": 0.01241333713643014,
  "tail_sensor_speed_mean_m_s": -0.012317711053464478,
  "tail_fk_speed_mean_m_s": -0.012282943418044893,
  "peak_tilt_rad": 0.10223488013404114,
  "peak_wheel_torque_nm": 0.29107558727264404,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 65.39581606298452
}
```
