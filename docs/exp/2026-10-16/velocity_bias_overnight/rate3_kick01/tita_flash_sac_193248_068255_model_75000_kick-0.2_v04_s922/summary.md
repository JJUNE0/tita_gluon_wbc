# tita_flash_sac_193248_068255_model_75000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "7e8027e25c167cc4c0f64f47bcb89915e23035f4ec8d3274fc3237f108eaa4b0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007396040894019084,
  "max_drift_m": 0.15865400123340734,
  "radial_IAE_m_s": 0.929148453324568,
  "signed_longitudinal_delta_m": -0.0073956725991391505,
  "tail_speed_mean_m_s": 2.93176249889007e-05,
  "tail_speed_rms_m_s": 2.9348904947225243e-05,
  "tail_sensor_speed_mean_m_s": 2.9411101911397503e-05,
  "tail_fk_speed_mean_m_s": 2.8979111904142218e-05,
  "peak_tilt_rad": 0.12396273889027554,
  "peak_wheel_torque_nm": 1.7435271739959717,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2780246081814856,
  "final_integral_m_s": -0.2780246081814856,
  "elapsed_wall_s": 15.807900412997697
}
```
