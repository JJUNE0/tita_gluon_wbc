# tita_flash_sac_193248_068255_model_55000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "a602b02259d723f7309dc5fc9d2f3eb0ba8c3b6cb65c377389e9db7e14ef85ec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029387351232524967,
  "max_drift_m": 0.07600879449467932,
  "radial_IAE_m_s": 1.656520818665571,
  "signed_longitudinal_delta_m": 0.029386915215482274,
  "tail_speed_mean_m_s": 8.636484065538325e-05,
  "tail_speed_rms_m_s": 8.638741324740138e-05,
  "tail_sensor_speed_mean_m_s": 8.671898388468586e-05,
  "tail_fk_speed_mean_m_s": 8.510078136822566e-05,
  "peak_tilt_rad": 0.13834384468098215,
  "peak_wheel_torque_nm": 0.7621662020683289,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.310724696685266,
  "final_integral_m_s": 0.3105699590343609,
  "elapsed_wall_s": 16.125025874003768
}
```
