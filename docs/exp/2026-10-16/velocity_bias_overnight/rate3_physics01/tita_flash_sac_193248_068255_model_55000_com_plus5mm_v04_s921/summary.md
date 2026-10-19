# tita_flash_sac_193248_068255_model_55000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "dd13c94a5ee1dc39815b8fb7ef122c1f081688d09df92781f2b7f0a333b60ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027980073839422328,
  "max_drift_m": 0.09348666225829577,
  "radial_IAE_m_s": 2.1420849618912365,
  "signed_longitudinal_delta_m": -0.027978454642936117,
  "tail_speed_mean_m_s": 0.0002377616989309064,
  "tail_speed_rms_m_s": 0.00023813323825803872,
  "tail_sensor_speed_mean_m_s": 0.00023758586471290012,
  "tail_fk_speed_mean_m_s": 0.00023634683276744825,
  "peak_tilt_rad": 0.14568432177983248,
  "peak_wheel_torque_nm": 1.0394492149353027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4003613220702801,
  "final_integral_m_s": 0.4003613220702801,
  "elapsed_wall_s": 9.680059255973902
}
```
