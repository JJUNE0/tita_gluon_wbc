# tita_flash_sac_115632_883848_model_85000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "cad1f6e990ae010256f9113175b8eb583d34fc0219eb70c6217f995a4adcbed8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09487471892486021,
  "max_drift_m": 0.10614646162761031,
  "radial_IAE_m_s": 5.646606354073697,
  "signed_longitudinal_delta_m": 0.0948725478281006,
  "tail_speed_mean_m_s": 5.652967726068371e-06,
  "tail_speed_rms_m_s": 7.604941987908023e-06,
  "tail_sensor_speed_mean_m_s": -5.458217798087505e-07,
  "tail_fk_speed_mean_m_s": 7.03924263812267e-06,
  "peak_tilt_rad": 0.06503047672490658,
  "peak_wheel_torque_nm": 0.562735915184021,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.634963799372759,
  "final_integral_m_s": 0.634963799372759,
  "elapsed_wall_s": 16.002272687968798
}
```
