# tita_flash_sac_193248_068255_model_25000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "318a3217be1da0644087458fa938c0f0bfa38f343700f79b9ded54903801cf4e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0172444380821848,
  "max_drift_m": 0.022270250857925496,
  "radial_IAE_m_s": 0.9967969707321787,
  "signed_longitudinal_delta_m": -0.017243067377810863,
  "tail_speed_mean_m_s": -1.670122058392968e-05,
  "tail_speed_rms_m_s": 1.676417047595485e-05,
  "tail_sensor_speed_mean_m_s": -1.6194874640226325e-05,
  "tail_fk_speed_mean_m_s": -1.7285830444627237e-05,
  "peak_tilt_rad": 0.13587442204251166,
  "peak_wheel_torque_nm": 0.6892752647399902,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.17763741233178673,
  "final_integral_m_s": -0.17760900508437427,
  "elapsed_wall_s": 18.03588044596836
}
```
