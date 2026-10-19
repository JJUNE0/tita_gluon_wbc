# tita_flash_sac_193248_068255_model_75000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
  "initial_physics_sha256": "65f788796424fec7cbddf1dbe4b2158af5557d1913ab4bd2063c41848ab4226c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0051499887842767315,
  "max_drift_m": 0.06633887835490007,
  "radial_IAE_m_s": 0.5095908992643029,
  "signed_longitudinal_delta_m": -0.005149000721405632,
  "tail_speed_mean_m_s": 3.141787140644566e-05,
  "tail_speed_rms_m_s": 3.147268093736155e-05,
  "tail_sensor_speed_mean_m_s": 3.152353937097666e-05,
  "tail_fk_speed_mean_m_s": 3.108342387865991e-05,
  "peak_tilt_rad": 0.07952915301693331,
  "peak_wheel_torque_nm": 1.5142006874084473,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27981185565986694,
  "final_integral_m_s": -0.27981185565986694,
  "elapsed_wall_s": 11.734467610018328
}
```
