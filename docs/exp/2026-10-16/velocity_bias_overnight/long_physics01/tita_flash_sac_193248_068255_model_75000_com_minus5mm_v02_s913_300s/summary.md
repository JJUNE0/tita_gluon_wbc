# tita_flash_sac_193248_068255_model_75000_com_minus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_minus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
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
  "final_drift_m": 0.03344654697022626,
  "max_drift_m": 0.06656282760264247,
  "radial_IAE_m_s": 10.1351555124144,
  "signed_longitudinal_delta_m": -0.033388504314996445,
  "tail_speed_mean_m_s": 3.3190182120531635e-06,
  "tail_speed_rms_m_s": 3.410699300261667e-06,
  "tail_sensor_speed_mean_m_s": 3.336408763559976e-06,
  "tail_fk_speed_mean_m_s": 3.1064277183370204e-06,
  "peak_tilt_rad": 0.09980394976757023,
  "peak_wheel_torque_nm": 1.1076393127441406,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.34613123281665714,
  "final_integral_m_s": -0.3461384152694365,
  "elapsed_wall_s": 41.16295476898085
}
```
