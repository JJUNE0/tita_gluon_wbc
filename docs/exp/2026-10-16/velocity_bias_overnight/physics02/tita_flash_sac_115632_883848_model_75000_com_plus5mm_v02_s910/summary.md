# tita_flash_sac_115632_883848_model_75000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "3ec39d3c7d030d2d25842cd6e1363a861585f0f5117009e05820226dbe8941a6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008511010690770596,
  "max_drift_m": 0.01093511024512509,
  "radial_IAE_m_s": 0.4946480854618364,
  "signed_longitudinal_delta_m": 0.0085028471582336,
  "tail_speed_mean_m_s": 1.0006133522679896e-05,
  "tail_speed_rms_m_s": 1.0824290980974267e-05,
  "tail_sensor_speed_mean_m_s": 9.99817031992926e-06,
  "tail_fk_speed_mean_m_s": 1.0897836866951763e-05,
  "peak_tilt_rad": 0.057042333192950156,
  "peak_wheel_torque_nm": 0.1828056424856186,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08244605305763864,
  "final_integral_m_s": 0.08243888417276078,
  "elapsed_wall_s": 13.950279911980033
}
```
