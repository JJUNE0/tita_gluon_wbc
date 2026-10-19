# tita_flash_sac_115632_883848_model_70000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "5fc1927ae4a3888df0ba86f9d05ac66da3347ab162707189b5c1303356e2998f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02406689925336564,
  "max_drift_m": 0.04984474857585687,
  "radial_IAE_m_s": 1.449071822593831,
  "signed_longitudinal_delta_m": -0.024058127887700887,
  "tail_speed_mean_m_s": -3.8572257046088254e-06,
  "tail_speed_rms_m_s": 3.887762878009432e-06,
  "tail_sensor_speed_mean_m_s": -4.113124420131584e-06,
  "tail_fk_speed_mean_m_s": -4.359592380550262e-06,
  "peak_tilt_rad": 0.09012324268171978,
  "peak_wheel_torque_nm": 0.7426385283470154,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2544524322305359,
  "final_integral_m_s": -0.2544448686284675,
  "elapsed_wall_s": 12.868790329957847
}
```
