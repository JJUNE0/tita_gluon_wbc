# tita_flash_sac_193248_068255_model_50000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "c4f2e5c18c51007811cf608e75906ba958c253f77607156ba16360034bd4683d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07153860808903206,
  "max_drift_m": 0.07153860808903206,
  "radial_IAE_m_s": 4.1815497174356935,
  "signed_longitudinal_delta_m": 0.07153618298969718,
  "tail_speed_mean_m_s": 3.923583139682852e-05,
  "tail_speed_rms_m_s": 3.943195447957131e-05,
  "tail_sensor_speed_mean_m_s": 3.8932453687331646e-05,
  "tail_fk_speed_mean_m_s": 4.011230872659393e-05,
  "peak_tilt_rad": 0.05644187952763091,
  "peak_wheel_torque_nm": 0.7884739637374878,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7252857390005402,
  "final_integral_m_s": 0.725189898216036,
  "elapsed_wall_s": 17.797968280036002
}
```
