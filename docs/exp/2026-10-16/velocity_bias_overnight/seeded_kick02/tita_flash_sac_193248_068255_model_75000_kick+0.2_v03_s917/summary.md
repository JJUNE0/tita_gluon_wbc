# tita_flash_sac_193248_068255_model_75000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "7465ac50b122481f12343d910466b605723f415e9921a374258c219650bb8437",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005059273419641485,
  "max_drift_m": 0.06614806976467386,
  "radial_IAE_m_s": 0.5061723715889968,
  "signed_longitudinal_delta_m": -0.0050585247422036544,
  "tail_speed_mean_m_s": 3.305232848244287e-05,
  "tail_speed_rms_m_s": 3.311080003674558e-05,
  "tail_sensor_speed_mean_m_s": 3.316652172570787e-05,
  "tail_fk_speed_mean_m_s": 3.271643695356841e-05,
  "peak_tilt_rad": 0.07965979230897147,
  "peak_wheel_torque_nm": 1.5091652870178223,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.28063730825070343,
  "final_integral_m_s": -0.28063730825070343,
  "elapsed_wall_s": 10.439570196031127
}
```
