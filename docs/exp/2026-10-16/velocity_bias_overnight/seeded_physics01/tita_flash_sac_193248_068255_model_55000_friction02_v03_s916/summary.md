# tita_flash_sac_193248_068255_model_55000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "e24070c2c8dbfaf165112b595c0ca23afcd5b7d10e028ee88e95fbab91d2282c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01603958677839841,
  "max_drift_m": 0.1295376969516786,
  "radial_IAE_m_s": 1.1594427627190445,
  "signed_longitudinal_delta_m": -0.0012815548823335355,
  "tail_speed_mean_m_s": -1.629930151465971e-05,
  "tail_speed_rms_m_s": 1.6300201936702372e-05,
  "tail_sensor_speed_mean_m_s": 0.00016220117325836648,
  "tail_fk_speed_mean_m_s": 1.8845996775867438e-07,
  "peak_tilt_rad": 0.15936729397851246,
  "peak_wheel_torque_nm": 0.990265429019928,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6109218253910639,
  "final_integral_m_s": 0.6109218253910639,
  "elapsed_wall_s": 10.753010477055795
}
```
