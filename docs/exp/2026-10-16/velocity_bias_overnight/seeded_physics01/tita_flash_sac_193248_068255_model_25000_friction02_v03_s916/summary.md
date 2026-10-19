# tita_flash_sac_193248_068255_model_25000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "de35b1a650b1470b69ed0710111c834247086cd51d276bed8bb6edc17b6f9180",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06193078369828222,
  "max_drift_m": 0.06769919315880303,
  "radial_IAE_m_s": 3.3578984731547674,
  "signed_longitudinal_delta_m": -0.06144909632839876,
  "tail_speed_mean_m_s": -6.946908149718896e-05,
  "tail_speed_rms_m_s": 0.0001116490404630791,
  "tail_sensor_speed_mean_m_s": -6.194702599892958e-05,
  "tail_fk_speed_mean_m_s": -6.821389012257435e-05,
  "peak_tilt_rad": 0.10829910322137781,
  "peak_wheel_torque_nm": 1.0245604515075684,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23686321282601103,
  "final_integral_m_s": 0.23686321282601103,
  "elapsed_wall_s": 10.775132893992122
}
```
