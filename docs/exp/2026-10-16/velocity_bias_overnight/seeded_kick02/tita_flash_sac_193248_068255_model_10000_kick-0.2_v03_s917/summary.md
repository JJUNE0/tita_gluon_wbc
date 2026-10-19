# tita_flash_sac_193248_068255_model_10000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
      "slew": 2.0,
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
  "initial_physics_sha256": "afb34808bdd5f78eee5334c8c02461d8a5a5636dff473cf20d3033a98906a294",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01754298011315454,
  "max_drift_m": 0.058449577290301064,
  "radial_IAE_m_s": 0.8791991406344393,
  "signed_longitudinal_delta_m": 0.01679723574565571,
  "tail_speed_mean_m_s": 0.0001756229428745213,
  "tail_speed_rms_m_s": 0.0001756322231327574,
  "tail_sensor_speed_mean_m_s": 0.00019025580548642738,
  "tail_fk_speed_mean_m_s": 0.0001972443910406745,
  "peak_tilt_rad": 0.040773248962414854,
  "peak_wheel_torque_nm": 3.862748622894287,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10568494005514638,
  "final_integral_m_s": 0.10568494005514638,
  "elapsed_wall_s": 9.533460656995885
}
```
