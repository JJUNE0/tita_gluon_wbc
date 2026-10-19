# tita_flash_sac_193248_068255_model_5000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "fb9f5e99a3e3fb72fad7315b30d63f21f6d5a113ebd87ef2b9f913908c755235",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.10646394632789453,
  "max_drift_m": 0.10646394632789453,
  "radial_IAE_m_s": 5.748821207285255,
  "signed_longitudinal_delta_m": -0.10481203666850619,
  "tail_speed_mean_m_s": 0.0003413803679067914,
  "tail_speed_rms_m_s": 0.00034144102956942194,
  "tail_sensor_speed_mean_m_s": 0.00017513221161906568,
  "tail_fk_speed_mean_m_s": 0.00012144525214825623,
  "peak_tilt_rad": 0.07399873188109107,
  "peak_wheel_torque_nm": 0.6536521911621094,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.9872557786139514,
  "final_integral_m_s": -0.987426688870138,
  "elapsed_wall_s": 13.768223954015411
}
```
