# tita_flash_sac_115632_883848_model_75000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "4918c0fa126ef5445cde50b626a92abc9f2c5b5847875d19d0039a117dae4876",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005649940818894171,
  "max_drift_m": 0.029382570842941307,
  "radial_IAE_m_s": 0.38754966099127885,
  "signed_longitudinal_delta_m": -0.005624463854755418,
  "tail_speed_mean_m_s": 2.2668704576038328e-05,
  "tail_speed_rms_m_s": 2.3048344678246025e-05,
  "tail_sensor_speed_mean_m_s": 2.2600730955675027e-05,
  "tail_fk_speed_mean_m_s": 2.3194933563472504e-05,
  "peak_tilt_rad": 0.06985693921551683,
  "peak_wheel_torque_nm": 0.46054497361183167,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.06546319756620539,
  "final_integral_m_s": -0.06551301860429201,
  "elapsed_wall_s": 15.119855207041837
}
```
