# tita_flash_sac_115632_883848_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "481cc5612b9661b07680b16abd556b34cbb9f36da5d3b34b6495e84171e99e60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.044147261839111954,
  "max_drift_m": 0.044147261839111954,
  "radial_IAE_m_s": 0.7229937304728541,
  "signed_longitudinal_delta_m": 0.044114476671920755,
  "tail_speed_mean_m_s": 0.0014272241819225343,
  "tail_speed_rms_m_s": 0.0014518298902972606,
  "tail_sensor_speed_mean_m_s": 0.0014242681066685972,
  "tail_fk_speed_mean_m_s": 0.0014247241329284446,
  "peak_tilt_rad": 0.052009174057000784,
  "peak_wheel_torque_nm": 0.03346031904220581,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.397759491985198
}
```
