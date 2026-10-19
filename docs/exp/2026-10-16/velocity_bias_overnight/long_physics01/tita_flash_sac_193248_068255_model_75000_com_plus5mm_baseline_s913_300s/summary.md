# tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "f18a1d608a686b461aea960ac47cbf520505f7687c03e648dc3cb075213c4ae4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 7.311369184637372,
  "max_drift_m": 14.253299692344665,
  "radial_IAE_m_s": 2508.138413527734,
  "signed_longitudinal_delta_m": 3.293876257736792,
  "tail_speed_mean_m_s": -0.012322153000401428,
  "tail_speed_rms_m_s": 0.012322154629366191,
  "tail_sensor_speed_mean_m_s": -0.012229040325956146,
  "tail_fk_speed_mean_m_s": -0.012213137885908448,
  "peak_tilt_rad": 0.10076977172743451,
  "peak_wheel_torque_nm": 0.29213207960128784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 28.901338887983
}
```
