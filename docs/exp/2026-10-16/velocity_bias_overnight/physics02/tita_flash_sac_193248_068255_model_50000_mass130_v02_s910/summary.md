# tita_flash_sac_193248_068255_model_50000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "2b32b499d647f06b1e8fdcdae06919855b3e95ee9085ac9bd3ab96ac96aaa950",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06530128050427021,
  "max_drift_m": 0.0703027340840604,
  "radial_IAE_m_s": 2.042062164637807,
  "signed_longitudinal_delta_m": -0.059945350183399845,
  "tail_speed_mean_m_s": -0.0010779284874956041,
  "tail_speed_rms_m_s": 0.04618120592812645,
  "tail_sensor_speed_mean_m_s": 0.00530242777277413,
  "tail_fk_speed_mean_m_s": 0.00038124302193060487,
  "peak_tilt_rad": 0.15930288979417195,
  "peak_wheel_torque_nm": 9.311407089233398,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.043159017526060925,
  "final_integral_m_s": -0.016934196839063546,
  "elapsed_wall_s": 17.414235046016984
}
```
