# tita_flash_sac_193248_068255_model_55000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "236ac936e96b9b10dc8f9452476defe9e6d0db468747bd65dfbb0371726c786f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023907453099492736,
  "max_drift_m": 0.07575907296395973,
  "radial_IAE_m_s": 1.8550404302607562,
  "signed_longitudinal_delta_m": -0.023905669639977294,
  "tail_speed_mean_m_s": 0.00021572704385109274,
  "tail_speed_rms_m_s": 0.00021573947277457123,
  "tail_sensor_speed_mean_m_s": 0.00021584981081812786,
  "tail_fk_speed_mean_m_s": 0.0002142033346208021,
  "peak_tilt_rad": 0.13777848160575057,
  "peak_wheel_torque_nm": 0.9192938804626465,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3072099162444287,
  "final_integral_m_s": 0.3072099162444287,
  "elapsed_wall_s": 8.507105719996616
}
```
