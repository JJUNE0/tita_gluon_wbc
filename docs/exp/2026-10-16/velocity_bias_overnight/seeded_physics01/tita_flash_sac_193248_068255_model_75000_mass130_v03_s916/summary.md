# tita_flash_sac_193248_068255_model_75000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "d7324f92d782fbbeb5de0b6b90d6be3eaca5fc61da04d75db4aa0539800d4720",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01828095098723358,
  "max_drift_m": 0.09966441707624037,
  "radial_IAE_m_s": 1.3101803929475504,
  "signed_longitudinal_delta_m": 0.018242417900360453,
  "tail_speed_mean_m_s": -3.817763311688787e-05,
  "tail_speed_rms_m_s": 0.004447856260717416,
  "tail_sensor_speed_mean_m_s": -8.986784254828954e-05,
  "tail_fk_speed_mean_m_s": 1.3064517508477802e-06,
  "peak_tilt_rad": 0.20582033797636812,
  "peak_wheel_torque_nm": 1.5156548023223877,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5052771946457422,
  "final_integral_m_s": -0.5052771946457422,
  "elapsed_wall_s": 13.384633055015001
}
```
