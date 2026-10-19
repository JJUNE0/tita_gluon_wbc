# tita_flash_sac_193248_068255_model_75000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "1581b9d41455b3348716060cfa3f77b88213d2b86f9e557cc372bc3ba827ce7b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03394236458424329,
  "max_drift_m": 0.06544550296092218,
  "radial_IAE_m_s": 2.054411865441361,
  "signed_longitudinal_delta_m": -0.03393782530353756,
  "tail_speed_mean_m_s": 7.689602954646768e-06,
  "tail_speed_rms_m_s": 7.690771017443456e-06,
  "tail_sensor_speed_mean_m_s": 7.822959785063569e-06,
  "tail_fk_speed_mean_m_s": 7.514295702273435e-06,
  "peak_tilt_rad": 0.09877746005942312,
  "peak_wheel_torque_nm": 1.0769846439361572,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35424635586486614,
  "final_integral_m_s": -0.35426143388211323,
  "elapsed_wall_s": 15.062078953022137
}
```
