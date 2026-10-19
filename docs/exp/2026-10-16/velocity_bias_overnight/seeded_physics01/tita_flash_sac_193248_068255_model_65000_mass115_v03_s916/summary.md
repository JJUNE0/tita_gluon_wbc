# tita_flash_sac_193248_068255_model_65000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "4dbe9c38deae01018a073ef5a858b0cadaaa70f5348e689d4da16b4778371bad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013844531147987728,
  "max_drift_m": 0.065847359285118,
  "radial_IAE_m_s": 0.9068686205452439,
  "signed_longitudinal_delta_m": -0.013834927518418404,
  "tail_speed_mean_m_s": 5.580394202537328e-06,
  "tail_speed_rms_m_s": 5.622312936361268e-06,
  "tail_sensor_speed_mean_m_s": 5.529143185046261e-06,
  "tail_fk_speed_mean_m_s": 6.002877061066821e-06,
  "peak_tilt_rad": 0.10256173132472601,
  "peak_wheel_torque_nm": 0.7019593119621277,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.401925427037107,
  "final_integral_m_s": -0.401925427037107,
  "elapsed_wall_s": 13.344756261038128
}
```
