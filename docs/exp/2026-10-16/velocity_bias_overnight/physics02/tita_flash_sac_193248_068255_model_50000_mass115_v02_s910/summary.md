# tita_flash_sac_193248_068255_model_50000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "adebfde77d3422b87e1d133e8d81e7e29b9750682643e1294ed1c2da79438f4b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022714934285465588,
  "max_drift_m": 0.024103155984300604,
  "radial_IAE_m_s": 0.5868269886125056,
  "signed_longitudinal_delta_m": -0.022701870448393956,
  "tail_speed_mean_m_s": -0.0008614910639652894,
  "tail_speed_rms_m_s": 0.021636878663859986,
  "tail_sensor_speed_mean_m_s": -0.0015982430533353425,
  "tail_fk_speed_mean_m_s": 0.00015268334991312796,
  "peak_tilt_rad": 0.08869082858245436,
  "peak_wheel_torque_nm": 7.036412239074707,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14992798352848596,
  "final_integral_m_s": 0.14031433216368577,
  "elapsed_wall_s": 15.58754321798915
}
```
