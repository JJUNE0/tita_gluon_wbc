# tita_flash_sac_193248_068255_model_75000_kick-0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "0d06512586c743b511737902eff841a0b8bca6a08df8f5d8fccd63b55c4ae84e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00719153332145133,
  "max_drift_m": 0.21625936312623673,
  "radial_IAE_m_s": 0.8677448816067765,
  "signed_longitudinal_delta_m": 0.0070709819726070475,
  "tail_speed_mean_m_s": 1.0011118248416314e-05,
  "tail_speed_rms_m_s": 1.006529240271566e-05,
  "tail_sensor_speed_mean_m_s": 1.0081125810254508e-05,
  "tail_fk_speed_mean_m_s": 9.687733999893633e-06,
  "peak_tilt_rad": 0.21137021551209956,
  "peak_wheel_torque_nm": 2.970261335372925,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27322942588775034,
  "final_integral_m_s": -0.27324438816089613,
  "elapsed_wall_s": 4.6750411910470575
}
```
