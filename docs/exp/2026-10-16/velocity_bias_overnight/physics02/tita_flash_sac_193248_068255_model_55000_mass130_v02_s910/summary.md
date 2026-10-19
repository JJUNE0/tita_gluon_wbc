# tita_flash_sac_193248_068255_model_55000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "b8140b72c0344490998c7e40faddf73fc28e8566aa7a3f49e882383543df1d99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011609567262306957,
  "max_drift_m": 0.021847102612795426,
  "radial_IAE_m_s": 0.6652949206872004,
  "signed_longitudinal_delta_m": 0.011607760666339192,
  "tail_speed_mean_m_s": 2.3439936076398097e-05,
  "tail_speed_rms_m_s": 2.345856450935108e-05,
  "tail_sensor_speed_mean_m_s": 2.3683338298693143e-05,
  "tail_fk_speed_mean_m_s": 2.3159201134496777e-05,
  "peak_tilt_rad": 0.18287696710539936,
  "peak_wheel_torque_nm": 0.5697307586669922,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12116664732212443,
  "final_integral_m_s": 0.12112009065674259,
  "elapsed_wall_s": 19.02591692103306
}
```
