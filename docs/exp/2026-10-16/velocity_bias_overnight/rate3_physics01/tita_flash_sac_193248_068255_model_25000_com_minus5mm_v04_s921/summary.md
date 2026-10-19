# tita_flash_sac_193248_068255_model_25000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "708e091eae3c1b579470048e57bf0389523d4317e36bcd212edf15853bed068e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029291929358502798,
  "max_drift_m": 0.05807386360933958,
  "radial_IAE_m_s": 1.6379184829216362,
  "signed_longitudinal_delta_m": -0.029291321074897257,
  "tail_speed_mean_m_s": -6.945589742882894e-05,
  "tail_speed_rms_m_s": 6.969035971945106e-05,
  "tail_sensor_speed_mean_m_s": -6.870619583963561e-05,
  "tail_fk_speed_mean_m_s": -6.877617972866505e-05,
  "peak_tilt_rad": 0.105862336418864,
  "peak_wheel_torque_nm": 1.2228559255599976,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3277271189790027,
  "final_integral_m_s": 0.3277271189790027,
  "elapsed_wall_s": 9.406715532008093
}
```
