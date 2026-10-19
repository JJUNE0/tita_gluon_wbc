# tita_flash_sac_193248_068255_model_10000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "e44375acf7d7ed33153816eba75bfc2a265b8f97b0b6f14b413e776431f4548a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018406226779444024,
  "max_drift_m": 0.05826996649061479,
  "radial_IAE_m_s": 0.9161988208495089,
  "signed_longitudinal_delta_m": 0.01772916098393255,
  "tail_speed_mean_m_s": 0.00017308234789307271,
  "tail_speed_rms_m_s": 0.00017313518346376899,
  "tail_sensor_speed_mean_m_s": 0.00018689676179251387,
  "tail_fk_speed_mean_m_s": 0.00019369916081259878,
  "peak_tilt_rad": 0.04071296381764822,
  "peak_wheel_torque_nm": 3.8598074913024902,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10976272102955545,
  "final_integral_m_s": 0.10976272102955545,
  "elapsed_wall_s": 7.812619819014799
}
```
