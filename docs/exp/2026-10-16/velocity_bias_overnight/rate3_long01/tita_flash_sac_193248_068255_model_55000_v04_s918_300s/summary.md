# tita_flash_sac_193248_068255_model_55000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "7007bd893858d3d846314c2b2aeb7490d4df2049ec6d1e6bb5affb8b926a23fa",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.020408675093305947,
  "max_drift_m": 0.07575912261384508,
  "radial_IAE_m_s": 4.76631701622288,
  "signed_longitudinal_delta_m": 0.0181186565330655,
  "tail_speed_mean_m_s": 0.000161149478180852,
  "tail_speed_rms_m_s": 0.0001629390486865039,
  "tail_sensor_speed_mean_m_s": 0.00015661612762913417,
  "tail_fk_speed_mean_m_s": 0.00015282687111151642,
  "peak_tilt_rad": 0.13777852572577576,
  "peak_wheel_torque_nm": 0.919309675693512,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.477304165141854,
  "final_integral_m_s": 0.477304165141854,
  "elapsed_wall_s": 27.12245042901486
}
```
