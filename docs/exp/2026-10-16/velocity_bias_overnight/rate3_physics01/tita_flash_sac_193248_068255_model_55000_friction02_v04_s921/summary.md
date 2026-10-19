# tita_flash_sac_193248_068255_model_55000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "78cd2ff23e87a08a3ac904ee75a7ba7d7e521867804947797063e5871724ef87",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013675953547059905,
  "max_drift_m": 0.11804003292470887,
  "radial_IAE_m_s": 1.0207894598641682,
  "signed_longitudinal_delta_m": -0.001680493661329111,
  "tail_speed_mean_m_s": -1.6300162644376428e-05,
  "tail_speed_rms_m_s": 1.6301013503811166e-05,
  "tail_sensor_speed_mean_m_s": 0.0001622008492460229,
  "tail_fk_speed_mean_m_s": 1.8722406474312512e-07,
  "peak_tilt_rad": 0.15934043094350248,
  "peak_wheel_torque_nm": 1.0894255638122559,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6109215787467369,
  "final_integral_m_s": 0.6109215787467369,
  "elapsed_wall_s": 9.826570556964725
}
```
