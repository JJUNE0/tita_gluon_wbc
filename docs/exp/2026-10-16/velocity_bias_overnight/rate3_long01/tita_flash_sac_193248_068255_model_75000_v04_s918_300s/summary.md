# tita_flash_sac_193248_068255_model_75000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "6ddc8383ae5c150daef6b624d38879830e4aba80fa6c2ff11118e2d1bd817420",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0029304208476096127,
  "max_drift_m": 0.055861093093413715,
  "radial_IAE_m_s": 1.5225649259278415,
  "signed_longitudinal_delta_m": -0.002229068157132551,
  "tail_speed_mean_m_s": 1.0441439088185028e-05,
  "tail_speed_rms_m_s": 1.0441731027738022e-05,
  "tail_sensor_speed_mean_m_s": 1.0418696458513468e-05,
  "tail_fk_speed_mean_m_s": 1.0086987621700148e-05,
  "peak_tilt_rad": 0.08530561314163787,
  "peak_wheel_torque_nm": 0.4399549663066864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2633505829639431,
  "final_integral_m_s": -0.2633505829639431,
  "elapsed_wall_s": 26.92214178899303
}
```
