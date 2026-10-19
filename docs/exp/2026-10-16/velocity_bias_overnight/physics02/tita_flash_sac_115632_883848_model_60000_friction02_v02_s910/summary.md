# tita_flash_sac_115632_883848_model_60000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "e050ff4c700506f3c38cf1efd297641aa7db7b53ccd2090bfaf787f2ea33d801",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00265658974040846,
  "max_drift_m": 0.007808292292716764,
  "radial_IAE_m_s": 0.20600236121759224,
  "signed_longitudinal_delta_m": 0.002555147356293443,
  "tail_speed_mean_m_s": 6.747705409138315e-07,
  "tail_speed_rms_m_s": 6.76984642190778e-07,
  "tail_sensor_speed_mean_m_s": -3.468276324003745e-05,
  "tail_fk_speed_mean_m_s": -6.087286709515595e-08,
  "peak_tilt_rad": 0.06149664958246848,
  "peak_wheel_torque_nm": 0.182821586728096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.042343080692740794,
  "final_integral_m_s": 0.042343365115800155,
  "elapsed_wall_s": 18.342665795003995
}
```
